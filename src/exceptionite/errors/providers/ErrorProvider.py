"""A Mail Service Provider."""


from masonite.provider import ServiceProvider
from .. import Handler, StackOverflowIntegration, SolutionsIntegration


class MasoniteHandler:

    def load_exception(self, e):
        from wsgi import container
        from masonite.response import Response
        response = container.make(Response)
        request = container.make('Request')
        handler = Handler(e)
        # handler.integrate(StackOverflowIntegration())
        handler.integrate(SolutionsIntegration())
        handler.context({
            'WSGI': {
                'Path': request.path,
                'Input': request.all() or None,
                'Parameters': request.url_params,
                'Request Method': request.get_request_method()
            },
            'Headers': self.get_headers(request)
        })

        return response.view(handler.render(), status=500)

    def get_headers(self, request):
        headers = {}
        for header, value in request.environ.items():
            if header.startswith('HTTP_'):
                headers.update({header: value})

        return headers

class ErrorProvider(ServiceProvider):

    wsgi = False

    def register(self):
        pass

    def boot(self):
        self.app.bind('ExceptionHandler', MasoniteHandler())
