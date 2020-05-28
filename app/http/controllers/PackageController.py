""" Welcome The User To Masonite """

from masonite.view import View
from masonite.request import Request
from app.User import User
from src.exceptionite.errors import Handler
from src.exceptionite.errors.TerminalHandler import TerminalHandler
from masonite.exceptions import ContainerError, InvalidCSRFToken
import pickle


class Throw:

    def __init__(self, z):
        y = x
        self.z = z
        raise ContainerError('Something Broke!')

class Fun:
    def func():
        pass
class PackageController:
    """Controller For Welcoming The User
    """

    def show(self, view: View, request: Request):
        try:
            Throw(view)
        except Exception as e:
            pass
            # exception = TerminalHandler(e)
        
        dic = {}

        # dic.update(['hello', 'world'])
        Fun()()

        return view.render('woh')



        
