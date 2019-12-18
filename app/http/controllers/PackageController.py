""" Welcome The User To Masonite """

from masonite.view import View
from masonite.request import Request
from app.User import User
from src.masonite.errors import Handler
from masonite.exceptions import ContainerError, InvalidCSRFToken
import pickle


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
            exception = Handler(e)
        
        raise InvalidCSRFToken("Invalid CSRF token.")
        dic = {}
        dic.update(['hello', 'world'])

        return view.render('woh')



        
