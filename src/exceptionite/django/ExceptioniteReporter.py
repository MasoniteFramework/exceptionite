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
        from django.http.response import HttpResponse

        handler = Handler()
        handler.start(self.exception)
        handler.render("terminal")
        handler.request = self.request
        handler.renderer("web").tab("context").add_blocks(ContextBlock)
        handler.renderer("web").tab("solutions").block("possible_solutions").register(
            *DjangoSolutions().get()
        )
        handler.set_options(OPTIONS)
        return HttpResponse(handler.render("web"))

    def get_traceback_json(self):
        from django.http.response import JsonResponse

        handler = Handler()
        handler.start(self.exception)
        handler.render("terminal")
        return JsonResponse(handler.render("json"))


class Exceptionite404Reporter:
    """Handle Django 404 errors specifically in debug mode."""

    def __init__(self):
        from mock import patch
        from django.http import HttpResponseNotFound

        patcher = patch(
            "django.views.debug.technical_404_response",
            lambda request, exception: HttpResponseNotFound(
                ExceptioniteReporter(request, None, exception, None).get_traceback_html()
            ),
        )
        patcher.start()
