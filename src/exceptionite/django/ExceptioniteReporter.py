from .. import Handler, Block
from .options import OPTIONS
from ..solutions import DjangoSolutions


class ContextBlock(Block):
    id = "django-request"
    name = "Context"
    icon = "DesktopComputerIcon"
    has_sections = True

    def build(self):
        from django.utils.version import get_version

        return {
            "Django": {
                "Version": get_version(),
            },
            "Request Info": {
                "Path": self.handler.request.path,
                "GET": self.handler.request.GET,
                "POST": self.handler.request.POST,
                "Files": self.handler.request.FILES,
                "Cookies": self.handler.request.COOKIES,
                "Request Method": self.handler.request.method,
            },
        }


class ExceptioniteReporter:
    def __init__(self, request, exc_type, exc_value, tb):
        self.request = request
        self.exception = exc_value

    def get_traceback_html(self):
        handler = Handler()
        handler.start(self.exception)
        handler.render("terminal")
        handler.request = self.request
        handler.renderer("web").tab("context").add_blocks(ContextBlock)
        handler.renderer("web").tab("solutions").block("possible_solutions").register(
            *DjangoSolutions().get()
        )
        handler.set_options(OPTIONS)
        return handler.render("web")
