import pprint
import inspect
import os
from typing import List

MARKER = "site-packages/"


class StackFrame:
    def __init__(
        self, index, frame_summary, variables={}, offset=5, shorten=False, absolute_path=""
    ):
        self.index = index
        self.file = frame_summary[0]
        self.relative_file = None
        self.is_vendor = False
        if shorten:
            rel_path = self.file.replace(f"{os.getcwd()}/", "")
            index = rel_path.find(MARKER)
            if index != -1:
                self.is_vendor = True
                self.relative_file = "~/" + rel_path[index + len(MARKER) :]
            else:
                self.relative_file = rel_path

        self.language = self.get_language(self.file)

        self.offset = offset
        self.lineno = frame_summary[1]
        self.offending_line = self.lineno
        self.parent_statement = frame_summary[2]
        self.statement = frame_summary[3]
        self.start_line = self.lineno - offset if (self.lineno - offset > 0) else 0
        self.end_line = self.lineno + offset
        self.variables = variables
        self.method = frame_summary.name if frame_summary.name != "<module>" else "__main__"

        with open(self.file) as fp:
            printer = pprint.PrettyPrinter(indent=4)

            self.file_contents = printer.pformat(fp.read()).split("\\n")[
                self.start_line : self.end_line
            ]

        formatted_contents = {}
        read_line = self.start_line + 1

        for content in self.file_contents:
            if self.language == "python":
                # content.replace("    ", "&nbsp;&nbsp;&nbsp;&nbsp;")
                formatted_line = (
                    content.replace("'\n '", "")
                    .replace("'\n \"", "")
                    .replace("\"\n '", "<br>")
                    .replace('"\n "', "")
                    .replace("""(\'""", "")
                    .replace("')", "")
                )
            else:
                formatted_line = content.replace("'\n '", "").replace("'\n \"", "")

            if self.statement in formatted_line:
                self.offending_line = read_line

            formatted_contents.update({read_line: formatted_line})
            read_line += 1
        # remove common higher indentation
        min_start_spaces = 1000
        for line in formatted_contents.values():
            if line != "":
                min_start_spaces = min(min_start_spaces, len(line) - len(line.lstrip(" ")))

        self.file_contents = {
            number: text[min_start_spaces:] for number, text in formatted_contents.items()
        }

    def get_language(self, file):
        if file.endswith(".py"):
            return "python"
        elif file.endswith(".html"):
            return "html"

        return "python"


class StackTrace:
    trace: List[StackFrame]

    def __init__(self, traceback, exception, offset=5, shorten=False) -> None:
        self.traceback = traceback
        self.exception = exception
        self.trace = []
        self.loop_index = 0
        # options
        self.offset = offset
        self.shorten = shorten

    def generate(self):
        traceback = []
        for index, tb in enumerate(self.traceback.stack):
            traceback.append(
                StackFrame(
                    index,
                    tb,
                    variables=tb.locals,
                    offset=self.offset,
                    shorten=self.shorten,
                )
            )

        if hasattr(self.exception, "from_obj"):
            frame_summary = [
                inspect.getsourcefile(self.exception.from_obj),
                inspect.getsourcelines(self.exception.from_obj)[1],
                "",
                "null",
            ]
            traceback.append(
                StackFrame(
                    len(traceback),
                    frame_summary,
                    variables={},
                    offset=self.offset,
                    shorten=self.shorten,
                )
            )

        self.trace = traceback
        return self.trace

    def __iter__(self):
        self.loop_index = 0
        return self

    def __next__(self):
        if self.loop_index < len(self.trace):
            result = self.trace[self.loop_index]
            self.loop_index += 1
            return result
        else:
            raise StopIteration

    def __len__(self):
        return len(self.trace)

    def reverse(self):
        self.trace.sort(key=lambda frame: frame.index, reverse=True)
        return self

    def unreverse(self):
        self.trace.sort(key=lambda frame: frame.index, reverse=False)
        return self

    def first(self):
        return self.trace[0]

    def serialize(self):
        stack_data = []
        for frame in self.trace:
            frame_data = {
                "index": frame.index,
                "no": frame.lineno,
                "file": frame.file,
                "relative_file": frame.relative_file,
                "is_vendor": frame.is_vendor,
                "language": frame.language,
                "start": frame.start_line,
                "content": frame.file_contents,
                "variables": frame.variables,
                "method": frame.method,
            }
            stack_data.append(frame_data)

        return stack_data
