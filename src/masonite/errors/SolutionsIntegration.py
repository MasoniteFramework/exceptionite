import os

import jinja2
import requests
from jinja2 import (ChoiceLoader, DictLoader, Environment, PackageLoader,
                    select_autoescape)
import re

class SolutionsIntegration:

    name = "Possible Solutions"
    count = 0
    solutions = {
        r'^dictionary update sequence element #': 
            """
            Looks like you are trying to update a dictionary but are actually using a set or a list to update the dictionary instead. Double check what you are passing into the update method
            """
        ,
        r'^division by zero': 
            """
            You cannot divide by zero. Check the denominator (the bottom number). Use the variables on the left under the stack traces to see if you can find any 0 values
            """
        ,
        r'^class \'(?P<class>([\w]*))\' has no attribute (?P<method>(\w+))': 
            """
            Check the :method attribute exists on the ':class' class. 
            """
        ,
        r"^\'([\w]+)\' object has no attribute 'controller'":
            """
            This error is because of either a syntax error in your controller or an invalid import at the top of your controller.
            """
        ,
        r"^invalid syntax \((?P<class>(\w+\.py))+, line (?P<line>(\w+))":
            """
            Syntax errors are usually simple to fix. Just find the place that has invalid Python syntax and fix it. A good place to look is in your :class file on line :line
            """
        ,
        r"^'(?P<object>(\w+))' object has no attribute '(?P<attribute>(\w+))'":
            """
            Double check the object you are using and make sure it has the :attribute attribute. 
            
            If you are using a builtin python type then check Python documentation. 
            If you are using your own class then check the available methods.
            """
        ,
        r"No module named '(?P<module>(\w+))'": 
            """
            This is an import error. Check the file where you imported the ":module" module. Make sure its spelled right and make sure you pip installed this module correctly if this is supposed to come from a PYPI package.
            """
        ,
        r"cannot import name '(?P<object>(\w+))'":
            """
            This is an import error. Check the file where you imported the ":object" class and make sure it exists there.
            """
        ,
        r"'(?P<object>(\w+))' object is not subscriptable":
            """
            Looks like you expected ":object" to be an iterable but it is not. You can only use subscrptions, like x[0], on iterable type objects (like lists, dicts, and strings) but not ":object" in this case.
            """
        ,
        r"Invalid CSRF token.":
            """
            CSRF tokens are used to make sure nobody is making requests to your web app from the outside. If you just submitted a form request make sure you put the {{ csrf_field }} inside the form tag
            """
        ,
    }

    def __init__(self):
        pass

    def content(self, handler):
        possible_solutions = []
        for pattern, solution in self.solutions.items():
            r = re.compile(pattern)
            if r.match(handler.message()):
                matches = [m.groupdict() for m in r.finditer(handler.message())]
                self.count += 1
                for code, replacement in matches[0].items():
                    solution = solution.replace(":"+code, replacement)

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
