from .. import Handler, Block
from .options import OPTIONS


class ContextBlock(Block):
    id = "flask"
    name = "Flask"
    icon = "DesktopComputerIcon"

    def build(self):
        return {
            "Path": self.handler.request.path,
            "Input": dict(self.handler.request.args),
            "Request Method": self.handler.request.method,
        }


class ExceptioniteReporter:
    def __init__(self, exception, request):
        self.exception = exception
        self.request = request
        handler = Handler()
        handler.renderer("web").tab("context").add_blocks(ContextBlock)
        handler.request = self.request
        handler.set_options(OPTIONS)

        handler.start(self.exception)
        self.handler = handler

    def html(self):
        return self.handler.render("web")

    def json(self):
        return self.handler.render("json")

    def terminal(self):
        return self.handler.render("terminal")
