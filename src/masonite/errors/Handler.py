import traceback
import sys
import jinja2
import pprint
import inspect
from jinja2 import ChoiceLoader, Environment, PackageLoader, select_autoescape

class Handler:

    def __init__(self, e=False):
        self.e = e
        self._contexts = {}
        self.scoped_variables = inspect.trace()[-1][0].f_locals
        self.type, self.value, self.tb  = exc_type, exc_value, exc_traceback = sys.exc_info()
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
        traceback = []
        for tb in self.traceback.stack:
            traceback.append(StackLine(tb, tb.locals))
        traceback.reverse()
        return traceback
    
    def context(self, context: dict):
        self._contexts.update(context)
        return self
        
    def context(self, context: dict):
        self._contexts.update(context)
        return self

    def get_contexts(self):
        return self._contexts
    
    def create_trace(self):
        traceback = []
        for tb in self.traceback.stack:
            traceback.append(StackLine(tb, tb.locals))

        return traceback
    
    def render(self):
        loader = ChoiceLoader(
            [PackageLoader('resources', 'templates')]
        )

        environment = Environment(
            loader=loader,
            autoescape=select_autoescape(['html', 'xml'])
        )
        return environment.get_template('exception.html').render({'exception': self})
        return 'hi'

class StackLine:

    def __init__(self, frame_summary, variables = {}):
        self.file = frame_summary[0]
        self.lineno = frame_summary[1]
        self.parent_statement = frame_summary[2]
        self.statement = frame_summary[3]
        self.start_line = self.lineno - 5
        self.end_line = self.lineno + 5
        # print('setting variables', variables)
        self.variables = variables

        with open(self.file) as fp:
            printer = pprint.PrettyPrinter(indent=4)
            self.file_contents = printer.pformat(fp.read()).split('\\n')[self.start_line:self.end_line]

        formatted_contents = {}
        read_line = self.start_line + 1
        for content in self.file_contents:
            formatted_line = (content
                    .replace('    ', '&nbsp;&nbsp;&nbsp;&nbsp;')
                    .replace("'\n '", '')
                    .replace('\'\n "', '')
                    .replace('"\n \'', '<br>')
                )

            for variable, value in variables.items():
                split = content.split(' ')
                if variable in split:
                    try:
                        formatted_line += " # {} == {}".format(variable, value)
                    except TypeError:
                        pass

            # print('finally adding', formatted_line)
            formatted_contents.update({read_line: formatted_line})
            read_line += 1
        # print(formatted_contents)
        self.file_contents = formatted_contents
