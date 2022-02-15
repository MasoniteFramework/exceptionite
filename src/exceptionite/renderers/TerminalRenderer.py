from colorama import init as init_colorama, Fore, Style
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Handler import Handler


COLORS_PREFIX = {
    "error": Fore.RED + Style.BRIGHT,
    "info": Fore.CYAN + Style.BRIGHT,
    "success": Fore.GREEN + Style.BRIGHT,
}


def color_output(color: str, output: str) -> str:
    return f"{COLORS_PREFIX.get(color)}{output}" + "\033[0m"


def get_frame_line_output(frame, index: int = None) -> str:
    frame_method = color_output("info", f"{frame.method}()")
    frame_line = f"{frame.relative_file or frame.file}: L{frame.lineno} in {frame_method}"
    if index:
        frame_index_colored = index if frame.is_vendor else color_output("success", index)
        return f"{frame_index_colored} {frame_line}"
    return frame_line


class TerminalRenderer:
    """Renderer used to print an exception nicely in the terminal. It will render stack
    trace too."""

    def __init__(self, handler: "Handler") -> None:
        self.handler = handler

    def render(self) -> str:
        """Print exception and stack trace nicely in terminal."""
        init_colorama()

        # start printing exception to terminal
        print("")
        print("")
        colored_exception_type = color_output("error", self.handler.exception())
        print(f"  {colored_exception_type}: {self.handler.message()}")
        print("")

        # show most recent frame of the stack
        stacktrace = self.handler.stacktrace().reverse()
        first_frame = stacktrace.first()
        first_frame_code = first_frame.file_contents
        print(f"   {get_frame_line_output(first_frame)}")
        print("")

        # get highest line number to align numbers with padding
        max_no_len = len(str(max(first_frame_code.keys())))
        for lineno, code_line in first_frame_code.items():
            lineno_str = str(lineno)
            if len(lineno_str) < max_no_len:
                for space in range(max_no_len - len(lineno_str)):
                    lineno_str += " "
            code_line = code_line.replace("&nbsp;", " ")
            # highlight line where exception raised
            if lineno == first_frame.offending_line:
                print(color_output("error", f" > {lineno_str} | {code_line}"))
            else:
                print(f"   {lineno_str} | {code_line}")
        print("")

        # show other frames
        title = color_output("info", f"Stack Trace ({len(stacktrace)}):")
        print(f"   {title}")
        print("")
        for index, frame in enumerate(stacktrace):
            frame_index = str(index + 1)
            print(f"   # {get_frame_line_output(frame, frame_index)}")
        return ""
