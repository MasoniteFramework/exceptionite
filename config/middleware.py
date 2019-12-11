""" Middleware Configuration Settings """

from masonite.middleware import ResponseMiddleware

from app.http.middleware.AuthenticationMiddleware import AuthenticationMiddleware
from app.http.middleware.CsrfMiddleware import CsrfMiddleware
from app.http.middleware.LoadUserMiddleware import LoadUserMiddleware

"""
|--------------------------------------------------------------------------
| HTTP Middleware
|--------------------------------------------------------------------------
|
| HTTP middleware is middleware that will be ran on every request. Middleware
| is only ran when a HTTP call is successful (a 200 response). This list
| should contain a simple aggregate of middleware classes.
|
"""

HTTP_MIDDLEWARE = [
    LoadUserMiddleware,
    CsrfMiddleware,
    ResponseMiddleware
]

"""
|--------------------------------------------------------------------------
| Route Middleware
|--------------------------------------------------------------------------
|
| Route middleware is middleware that is registered with a name and can
| be used in the routes/web.py file. This middleware should really be
| used for middleware on an individual route like a dashboard route.
|
| The Route Middleware is a dictionary with the key being what is specified
| in your route/web.py file (in the .middleware() method) and the value is
| a string with the full module path of the middleware class
|
"""

ROUTE_MIDDLEWARE = {
    'auth':  AuthenticationMiddleware,
}
