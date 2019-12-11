import traceback
import sys
import jinja2
import pprint

class Handler:

    def __init__(self, e=False):
        self.e = e
        self.type, self.value, self.tb  = exc_type, exc_value, exc_traceback = sys.exc_info()
        self.traceback = traceback.TracebackException(self.type, self.value, self.tb)
        self.trace = self.create_trace()

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
            traceback.append(StackLine(tb))
        traceback.reverse()
        return traceback
    
    def create_trace(self):
        traceback = []
        for tb in self.traceback.stack:
            traceback.append(StackLine(tb))

        return traceback
    
    def render(self):
        return 'exceptions'

class StackLine:

    def __init__(self, frame_summary):
        self.file = frame_summary[0]
        self.lineno = frame_summary[1]
        self.parent_statement = frame_summary[2]
        self.statement = frame_summary[3]
        start_line = self.lineno - 5
        end_line = self.lineno + 5
        with open(self.file) as fp:
            printer = pprint.PrettyPrinter(indent=4)
            self.file_contents = printer.pformat(fp.read()).split('\\n')[start_line:end_line]
        formatted_contents = {}
        read_line = start_line + 1
        for content in self.file_contents:
            formatted_line = (content
                    .replace('    ', '&nbsp;&nbsp;&nbsp;&nbsp;')
                    .replace("'\n '", '')
                    .replace('\'\n "', '')
                    .replace('"\n \'', '<br>')
                )

            formatted_contents.update({read_line: formatted_line})
            read_line += 1
            print(formatted_contents)

        self.file_contents = formatted_contents
