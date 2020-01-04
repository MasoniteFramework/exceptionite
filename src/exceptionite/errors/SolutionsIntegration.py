import os

import jinja2
import requests
from jinja2 import (ChoiceLoader, DictLoader, Environment, PackageLoader,
                    select_autoescape)
import re

class DictionaryUpdateSequence:

    def title(self):
        return "Problem title"
    
    def description(self):
        return "Looks like you are trying to update a dictionary but are actually using a set or a list to update the dictionary instead. Double check what you are passing into the update method"

    def regex(self):
        return r'^dictionary update sequence element #'
        
class ClassMethodExists:

    def title(self):
        return "Class Method Exists"
    
    def description(self):
        return (
            "Check the :method attribute exists on the ':class' class. If this is a class you made then check the file its in and see if the method exists."
            "If this is a third party class then refer to the documentation."
            )

    def regex(self):
        return r'^class \'(?P<class>([\w]*))\' has no attribute (?P<method>(\w+))'

class GetAttributeObject:

    def title(self):
        return "Class Method Exists"
    
    def description(self):
        return (
            """
            Double check the object you are using and make sure it has the :attribute attribute. 
            
            If you are using a builtin python type then check Python documentation. 
            If you are using your own class then check the available methods.
            """
            )

    def regex(self):
        return r"^'(?P<object>(\w+))' object has no attribute '(?P<attribute>(\w+))'"

class GetAttributeController:

    def title(self):
        return "Class Method Exists"
    
    def description(self):
        return (
            "This error is because of either a syntax error in your controller or an invalid import at the top of your controller."
            )

    def regex(self):
        return r"^\'([\w]+)\' object has no attribute 'controller'"

class NoModuleNamed:

    def title(self):
        return "Module Not Found Error"
    
    def description(self):
        return (
            "This is an import error. Check the file where you imported the ': module' module. Make sure its spelled right and make sure you pip installed this module correctly if this is supposed to come from a PYPI package."
            )

    def regex(self):
        return r"No module named '(?P<module>(\w+))'"

class Syntax:

    def title(self):
        return "Syntax Error"
    
    def description(self):
        return (
            "Syntax errors are usually simple to fix. Just find the place that has invalid Python syntax and fix it. A good place to look is in your :class file on line :line"
            )

    def regex(self):
        return r"^invalid syntax \((?P<class>(\w+\.py))+, line (?P<line>(\w+))"


class ImportIssue:

    def title(self):
        return "Import Issue"

    def description(self):
        return (
            "This is an import error. Check the file where you imported the ':object' class and make sure it exists there."
        )

    def regex(self):
        return r"^cannot import name '(?P<object>(\w+))'"


class Undefined:

    def title(self):
        return "Undefined Variable"

    def description(self):
        return (
            "You are trying to use a variable that cannot be found. Check the ':variable' variable and see if it is declared, imported or in the correct scope depending on what the variable is."
        )

    def regex(self):
        return r"name '(?P<variable>(\w+))' is not defined"

class WrongParameterCount:

    def title(self):
        return "Wrong Parameter Count"

    def description(self):
        return (
            "You have the wrong amount of parameters for the ':object' object. "
            "It requires :correct parameters but you gave :wrong parameters. If the parameters are stored in a variable try checking the variable to the left. "
            "If you are passing variables in normally then check the signature of the object"
        )

    def regex(self):
        return r"^(?P<object>(\w*))\(\) takes (?P<correct>(\d+)) positional (argument|arguments) but (?P<wrong>(\d+)) (were|was) given"

class WrongConstructorParameterCount:

    def title(self):
        return "Wrong Parameters to a Constructor"

    def description(self):
        return (
            "The ':object' object doesn't take parameters but you gave some anyway. "
            "Check the constructor of the ':object' object. It's likely it does not take any parameters. "
            "If its stored in a variable you can check the value to the left."
        )

    def regex(self):
        return r"^(?P<object>(\w*))\(\) takes no parameters "

class ObjectNotCallable:

    def title(self):
        return "Objects Cannot Be Called"

    def description(self):
        return (
            "You cannot call objects. The ':object' object has already been instiatiated. " 
            "Once an object is instantiated it cannot be called directly anymore. "
            "Check if the ':object' is instantiated already."
        )

    def regex(self):
        return r"^'(?P<object>(\w*))' object is not callable"

class CSRFIssue:

    def title(self):
        return "CSRF Issue"
    
    def description(self):
        return (
            "CSRF tokens are used to make sure nobody is making requests to your web app from the outside. If you just submitted a form request make sure you put the {{ csrf_field }} inside the form tag"
            )

    def regex(self):
        return r"^Invalid CSRF token."

class SubscriptableIssue:

    def title(self):
        return "Object Not Subscriptable"
    
    def description(self):
        return (
            "Looks like you expected ':object' to be an iterable but it is not. You can only use subscrptions, like x[0], on iterable type objects (like lists, dicts, and strings) but not ':object' in this case."
            )

    def regex(self):
        return r"^'(?P<object>(\w+))' object is not subscriptable"

class SolutionsIntegration:

    name = "Possible Solutions"
    count = 0

    def __init__(self):
        self.registered_solutions = []
        self.register(
            DictionaryUpdateSequence(), 
            ClassMethodExists(),
            GetAttributeObject(),
            GetAttributeController(),
            NoModuleNamed(),
            Syntax(),
            ImportIssue(),
            CSRFIssue(),
            Undefined(),
            WrongParameterCount(),
            WrongConstructorParameterCount(),
            ObjectNotCallable(),
            SubscriptableIssue(),
        )

    def content(self, handler):
        possible_solutions = []
        for solution in self.registered_solutions:
            r = re.compile(solution.regex())
            if r.match(handler.message()):
                description = solution.description()
                matches = [m.groupdict() for m in r.finditer(handler.message())]
                self.count += 1
                for code, replacement in matches[0].items():
                    description = description.replace(":"+code, replacement)

                solution.modified_description = description
                possible_solutions.append(solution)

        current_path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_path, 'templates/solutions.html'), 'r') as f:
            overflow_exception = f.read()

        loader = DictLoader({
            'solutions.html': overflow_exception,
        })

        environment = Environment(
            loader=loader,
            autoescape=select_autoescape(['html', 'xml'])
        )
        return environment.get_template('solutions.html').render({'solutions': possible_solutions})

    def register(self, *solutions):
        self.registered_solutions += solutions
        return self

