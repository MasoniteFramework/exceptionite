import inspect
import math
import pprint
import sys
import traceback
import os

import jinja2
from jinja2 import ChoiceLoader, Environment, PackageLoader, select_autoescape, DictLoader


class Handler:

    def __init__(self, e=False, **kwargs):
        self.e = e
        self._contexts = {}
        self.type, self.value, self.tb = exc_type, exc_value, exc_traceback = sys.exc_info()
        self.traceback = traceback.TracebackException(
            self.type, self.value, self.tb, capture_locals=True)
        self.trace = self.create_trace()

        self.python_version = str(
            sys.version_info[0]) + '.' + str(sys.version_info[1]) + '.' + str(sys.version_info[2])
        self.default_encoding = sys.getdefaultencoding()
        self.file_system_encoding = sys.getfilesystemencoding()
        self.platform = sys.platform

        self.context({
            'Environment & Details': {
                'Python Version': self.python_version,
                'Platform': self.platform,
                'File System Encoding': self.file_system_encoding,
                'Default Encoding': self.default_encoding
            }
        })

    def any(self):
        return bool(self.e)

    def count(self):
        return len(self.trace)

    def message(self):
        return str(self.e)

    def exception(self):
        return self.e.__class__.__name__

    def namespace(self):
        return self.e.__class__.__module__ + '.' + self.exception()

    def stacktrace(self):
        traceback = self.trace
        traceback.reverse()
        return traceback

    def context(self, context: dict):
        self._contexts.update(context)
        return self

    def get_contexts(self):
        return self._contexts

    def create_trace(self):
        traceback = []
        for tb in self.traceback.stack:
            traceback.append(StackLine(tb, variables=tb.locals))

        return traceback

    def render(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_path, 'templates/exception.html'), 'r') as f:
            exception_template = f.read()

        with open(os.path.join(current_path, 'templates/css/tailwind.css'), 'r') as f:
            tailwind_template = f.read()

        with open(os.path.join(current_path, 'templates/css/prism.css'), 'r') as f:
            prism_template = f.read()

        loader = DictLoader({
            'exception.html': exception_template,
            'css/tailwind.css': tailwind_template,
            'css/prism.css': prism_template,
        })

        environment = Environment(
            loader=loader,
            autoescape=select_autoescape(['html', 'xml'])
        )

        return environment.get_template('exception.html').render({'exception': self})


class StackLine:

    def __init__(self, frame_summary, variables={}):
        self.file = frame_summary[0]
        self.language = self.get_language(self.file)

        # Cut off 30% of the string
        self.file_short = '..' + self.file[math.floor(len(self.file) * .30):]
        self.lineno = frame_summary[1]
        self.offending_line = self.lineno
        self.parent_statement = frame_summary[2]
        self.statement = frame_summary[3]
        self.start_line = self.lineno - 5
        self.end_line = self.lineno + 5
        self.variables = variables

        with open(self.file) as fp:
            printer = pprint.PrettyPrinter(indent=4)

            self.file_contents = printer.pformat(fp.read()).split('\\n')[
                self.start_line:self.end_line]

        formatted_contents = {}
        read_line = self.start_line + 1
        for content in self.file_contents:
            if self.language == 'python':
                formatted_line = (content
                                  .replace('    ', '&nbsp;&nbsp;&nbsp;&nbsp;')
                                  .replace("'\n '", '')
                                  .replace('\'\n "', '')
                                  .replace('"\n \'', '<br>')
                                  .replace('"\n "', '')
                                  )
            else:
                formatted_line = (content
                                  .replace("'\n '", '')
                                  .replace('\'\n "', ''))
            if self.statement in formatted_line:
                self.offending_line = read_line

            formatted_contents.update({read_line: formatted_line})
            read_line += 1

        self.file_contents = formatted_contents

    def get_language(self, file):
        if file.endswith('.py'):
            return 'python'
        elif file.endswith('.html'):
            return 'html'

        return 'python'
