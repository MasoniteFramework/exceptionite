import inspect
import json
import pprint
import os
from typing import List
import sys


class StackFrame:
    """Model a frame in the stack trace."""

    def __init__(self, index, frame_summary, variables={}, offset=5, shorten=False):
        self.index = index
        self.file = frame_summary[0]
        self.relative_file = None
        self.is_vendor = False

        # frame filename string should be shorten
        if shorten:
            rel_path = self.file.replace(f"{os.getcwd()}/", "")

            # check if frame is a vendor frame (from an external python package or masonite package
            # in development)
            if rel_path.startswith(sys.base_prefix) or rel_path.startswith(sys.exec_prefix):
                self.is_vendor = True
                self.relative_file = "~/" + rel_path.lstrip(sys.base_prefix)
            elif rel_path.find("src/masonite/") != -1:
                self.is_vendor = True
                cut_index = rel_path.find("src/masonite/") + len("src/")
                self.relative_file = "~/" + rel_path[cut_index:]
            else:  # it's located in project
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

        with open(self.file, "r", encoding="utf-8") as fp:
            printer = pprint.PrettyPrinter(indent=4)

            self.file_contents = printer.pformat(fp.read()).split("\\n")[
                self.start_line : self.end_line  # noqa: E203
            ]

        formatted_contents = {}
        read_line = self.start_line + 1

        for content in self.file_contents:
            if self.language == "python":
                formatted_line = (
                    content.replace("'\n '", "")
                    .replace("'\n \"", "")
                    .replace("\"\n '", "")
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

    def get_language(self, file: str) -> str:
        """Resolve language from the file path."""
        if file.endswith(".py"):
            return "python"
        elif file.endswith(".html"):
            return "html"

        return "python"


class StackTrace:
    """Model a stack trace."""

    trace: List["StackFrame"]

    def __init__(self, traceback, exception, offset=5, shorten=False, scrubber=None) -> None:
        self.traceback = traceback
        self.exception = exception
        self.trace = []
        self.loop_index = 0
        # options
        self.offset = offset
        self.shorten = shorten
        self.scrubber = scrubber

    def generate(self) -> List["StackFrame"]:
        """Generate all required data from a given traceback."""
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

    def __getitem__(self, index: int) -> "StackFrame":
        return self.trace[index]

    def reverse(self) -> "StackTrace":
        """Set stack frame in reversed order. Exception is located at the beginning."""
        self.trace.sort(key=lambda frame: frame.index, reverse=True)
        return self

    def unreverse(self) -> "StackTrace":
        """Set stack frame in normal order. Exception is located at the end."""
        self.trace.sort(key=lambda frame: frame.index, reverse=False)
        return self

    def first(self) -> "StackFrame":
        """Get first frame of the stack trace."""
        return self.trace[0]

    def serialize(self) -> dict:
        """Serialize all data from the stack trace."""
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
                "variables": self.scrubber(frame.variables),
                "method": frame.method,
            }
            stack_data.append(frame_data)

        return stack_data

    def serialize_light(self) -> dict:
        """Serialize some data from the stack trace, to get a compact representation."""
        stack_data = []
        for frame in self.trace:
            frame_data = {
                "index": frame.index,
                "file": frame.file,
                "line": frame.lineno,
                "statement": frame.parent_statement,
            }
            stack_data.append(frame_data)
        return stack_data
