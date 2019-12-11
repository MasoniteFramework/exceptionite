""" Welcome The User To Masonite """

from masonite.view import View
from masonite.request import Request
from app.User import User
from src.masonite.errors import Handler
from masonite.exceptions import ContainerError

class Throw:

    def __init__(self):
        raise ContainerError('Something Broke!')

class PackageController:
    """Controller For Welcoming The User
    """

    def show(self, view: View, request: Request):
        try:
            Throw()
        except Exception as e:
            print(e.__class__.__module__)
            exception = Handler(e)
        
        return view.render('exception', {'exception': exception})
        # return 'Hello World'
