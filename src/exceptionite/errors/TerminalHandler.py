from .Handler import Handler
from tabulate import tabulate
from colorama import init
from colorama import Fore, Back, Style


class TerminalHandler(Handler):
    def render(self):
        print("")
        table = []
        print("")
        print("    ", self.exception(), "-", self.message())
        print("")
        init()
        # print('  ', 'at', stack.file, 'on line', stack.lineno)
        first_stack = self.stacktrace()[0]
        for line in first_stack.file_contents.items():
            lineno, file_line = line
            table.append(["lineno", lineno])

            if lineno == first_stack.offending_line:
                print(
                    Fore.RED + Style.BRIGHT,
                    "",
                    "",
                    ">",
                    str(lineno),
                    "|",
                    file_line.replace("&nbsp;", " "),
                    "\033[0m",
                )
            else:
                print("  ", " ", str(lineno), "|", file_line.replace("&nbsp;", " "))
        print("")
        print("Stack Trace:")
        print("")
        for index, stack in enumerate(self.stacktrace()):
            print("  ", "# " + str(index + 1), stack.file, "on line", stack.lineno)
