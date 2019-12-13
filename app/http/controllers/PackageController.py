""" Welcome The User To Masonite """

from masonite.view import View
from masonite.request import Request
from app.User import User
from src.masonite.errors import Handler
from masonite.exceptions import ContainerError
import pickle

x = 2
class Throw:

    def __init__(self, z):
        y = x
        self.z = z
        raise ContainerError('Something Broke!')

class PackageController:
    """Controller For Welcoming The User
    """

    def show(self, view: View, request: Request):
        try:
            Throw(view)
        except Exception as e:
            print(e.__class__.__module__)
            exception = Handler(e)
        
        # exception.context({
        #     'WSGI': {
        #         'Path': request.path,
        #         'Input': request.all()
        #     }
        # })

        # return exception.render()
            
        return view.render('exception', {'exception': exception})
        # return 'Hello World'
