"""A Mail Service Provider."""


from masonite.provider import ServiceProvider
from masonite.errors import Handler


class MasoniteHandler:

    def load_exception(self, e):
        from wsgi import container
        from masonite.response import Response
        response = container.make(Response)
        request = container.make('Request')
        handler = Handler(e)
        handler.context({
            'WSGI': {
                'Path': request.path,
                'Input': request.all()
            }
        })
        response.view(handler.render(), status=500)


class ErrorProvider(ServiceProvider):

    wsgi = False

    def register(self):
        pass

    def boot(self):
        self.app.bind('ExceptionHandler', MasoniteHandler())
