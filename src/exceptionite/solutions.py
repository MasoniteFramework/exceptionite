# flake8: noqa: E501


class PythonSolutions:
    @classmethod
    def get(cls):
        return [
            DictionaryUpdateSequence(),
            DictionaryUpdateSequenceWithList(),
            ClassMethodExists(),
            UnexpectedEndBlock(),
            QueryDefaultValue(),
            NoRelationExistsInDatabase(),
            NoColumnExistsOnWhere(),
            NoColumnExistsOnWhereSQLite(),
            NoColumnExistsOnSelect(),
            UnsupportedOperand(),
            DivisionByZeroError(),
            GetAttributeObject(),
            ModuleHasNoAttribute(),
            ModuleNotCallable(),
            NoModuleNamed(),
            Syntax(),
            ImportIssue(),
            Undefined(),
            WrongParameterCount(),
            WrongConstructorParameterCount(),
            ObjectNotCallable(),
            SubscriptableIssue(),
            StringIndicesMustBeIntegers(),
            MySQLConnectionRefused(),
            PostgresConnectionRefused(),
            PostgresConnectionFailed(),
            DatabaseDoesNotExist(),
            DatabaseUserDoesNotExist(),
        ]


class MasoniteSolutions:
    @classmethod
    def get(cls):
        return [
            ClassModelMethodExists(),
            ImportIssueWithController(),
            IncorrectControllerName(),
            IncorrectlyDefinedRoute(),
            RouteNameNotFound(),
            IncludedTemplateNotFound(),
            ContainerKeyNotFoundRegister(),
            ContainerKeyNotFoundServiceProvider(),
            NotFound404(),
            InvalidRouteMethodType(),
            ModelNotFound(),
            DatabaseDriverNotFound(),
            DriverNotFound(),
        ]


class DjangoSolutions:
    @classmethod
    def get(cls):
        return [
            DjangoTemplateNotFound(),
            ContextShouldBeList(),
            RenderArgumentsOutOfOrder(),
        ]


class DictionaryUpdateSequence:
    def title(self):
        return "Updating a dictionary with a set. "

    def description(self):
        return (
            "Looks like you are trying to update a dictionary but are actually using a set. "
            "Double check what you are passing into the update method"
        )

    def regex(self):
        return r"dictionary update sequence element #0 has length 3; 2 is required"


class DictionaryUpdateSequenceWithList:
    def title(self):
        return "Updating a dictionary with a list or set. "

    def description(self):
        return (
            "Looks like you are trying to update a dictionary but are actually using a list or a set. "
            "Double check what you are passing into the dictionaries update method"
        )

    def regex(self):
        return r"cannot convert dictionary update sequence element #0 to a sequence"


class ClassMethodExists:
    def title(self):
        return "Check the class method exists"

    def description(self):
        return (
            "Check the :method attribute exists on the ':class' class. If this is a class you made then check the file its in and see if the method exists."
            "If this is a third party class then refer to the documentation."
        )

    def regex(self):
        return r"^class \'(?P<class>([\w]*))\' has no attribute (?P<method>(\w+))"


class ClassModelMethodExists:
    def title(self):
        return "Model method does not exist"

    def description(self):
        return "Could not find the ':method' method on the model class. Please check spelling. If this is a method you expect to be on the builder class then check the ORM documentation"

    def regex(self):
        return r"^class model \'(?P<class>([\w]*))\' has no attribute (?P<method>(\w+))"


class ImportIssueWithController:
    def title(self):
        return "Import Error In Controller"

    def description(self):
        return (
            "The :class controller could not be loaded into the route correctly. Check any recent imports or all imports in the controller. "
            "Worst case is you can import the controller directly in the route and you should get a python error."
        )

    def regex(self):
        return r"named (?P<class>([\w]*)) has been found in"


class IncorrectControllerName:
    def title(self):
        return "Mispelled Controller name"

    def description(self):
        return "The :class controller could be mispelled. Check your routes file for :class and make sure that is the correct spelling."

    def regex(self):
        return r"named (?P<class>([\w]*)) has been found in"


class IncorrectlyDefinedRoute:
    def title(self):
        return "Check the controller and action is set correctly on the route."

    def description(self):
        return "Check the definition on the controller is correct. If using string controllers it should be in the format of 'Controller@action'"

    def regex(self):
        return r"named (?P<class>([\w]*)) has been found in"

    def documentation_link(self):
        return "https://docs.masoniteproject.com/the-basics/routing#creating-a-route"


class RouteNameNotFound:
    def title(self):
        return "Check the the name exists in your routes file"

    def description(self):
        return """Check the routes file and make sure there is a route with the ".name(':name')\" method. You can also run `python craft routes:list` to see a table of routes. Check for your named route in that table."""

    def regex(self):
        return r"Could not find route with the name \'(?P<name>([\w]*))\'"

    def documentation_link(self):
        return "https://docs.masoniteproject.com/the-basics/routing#name"


class IncludedTemplateNotFound:
    def title(self):
        return "Check any imported templates inside the :name template."

    def description(self):
        return (
            "The :name template was found but a template included inside the :name template was not found. "
            "Check any lines of code that use the extends or include Jinja2 tags inside your template. "
            "Check the template path is correct. Included templates are absolute from your template directory and should end with '.html'"
        )

    def regex(self):
        return (
            r"One of the included templates in the \'(?P<name>([\w]*))\' view could not be found"
        )


class UnexpectedEndBlock:
    def title(self):
        return "Check the :name was closed correctly."

    def description(self):
        return "The error could be difficult to find so check ALL :name tags and make sure the :name tag is opened and closed correctly. "

    def regex(self):
        return r"Unexpected end of template. Jinja was looking for the following tags: \'(?P<name>([\w]*))\'."


class QueryDefaultValue:
    def title(self):
        return "Missing default value for ':field'"

    def description(self):
        return (
            "Default values are typically set on the database level. "
            "You can either add a default value on the :field table column in a migration or you should pass a value when creating this record"
        )

    def regex(self):
        return r"\(1364\, \"Field \'(?P<field>([\w]*))\' doesn't have a default value\"\)"


class NoColumnExistsOnWhere:
    def title(self):
        return "Check the table for the :field column"

    def description(self):
        return "Could not find the :field column. Check your 'where' clauses. Is :field on the table you are trying to query? Did you run the migrations yet? Maybe it was not spelled correctly?"

    def regex(self):
        return r"Unknown column \'(?P<field>([\w\.]*))\' in \'where clause\'"


class NoRelationExistsInDatabase:
    def title(self):
        return "The table ':table' does not exist in database"

    def description(self):
        return "Could not find the table ':table' in the database. Did you run the migrations yet? Maybe the table was not spelled correctly?"

    def regex(self):
        return r"relation \"(?P<table>([\w\.]*))\" does not exist"


class NoColumnExistsOnWhereSQLite:
    def title(self):
        return "Check the table for the :field column"

    def description(self):
        return "Could not find the :field column. Is :field on the table you are trying to query? Did you run the migrations yet? Maybe it was not spelled correctly?"

    def regex(self):
        return r"no such column: (?P<field>([\w\.]*))"


class NoColumnExistsOnSelect:
    def title(self):
        return "Check the table for the :field column"

    def description(self):
        return "Could not find the :field column. Check your 'select' clauses. Is :field on the table you are trying to query? Did you run the migrations yet? Maybe it was not spelled correctly?"

    def regex(self):
        return r"Unknown column \'(?P<field>([\w\.]*))\' in \'field list\'"


class UnsupportedOperand:
    def title(self):
        return "Trying to do math for values that are not of the same type (:type1 and :type2)"

    def description(self):
        return "Check the type of the 2 types. One is of type :type1 and the the other is of type :type2. They both need to be the same type"

    def regex(self):
        return r"unsupported operand type\(s\) for \+\: '(?P<type1>([\w\.]*))' and '(?P<type2>([\w\.]*))'"


class MySQLConnectionRefused:
    def title(self):
        return "Check database is running and connection details are correct"

    def description(self):
        return "Check that MySQL server is running and that MySQL configuration is correct (check that port, hostname, username and password are set correctly, and that environment variables are correctly defined)."

    def regex(self):
        return r"Can\'t connect to MySQL server"


class PostgresConnectionRefused:
    def title(self):
        return "Check database is running and connection details are correct"

    def description(self):
        return "Check that PostgresSQL server is running and that PostgresSQL configuration is correct (check that port=:port, hostname=:host, username and host are set correctly, and that environment variables are correctly defined)."

    def regex(self):
        return r"connection to server at \"(?P<host>([\w\.]*))\", port (?P<port>([\d]*)) failed"


class PostgresConnectionFailed:
    def title(self):
        return "Check database is running and connection details are correct"

    def description(self):
        return "Check that PostgresSQL server is running and that PostgresSQL configuration is correct (check that port, hostname, username and host are set correctly, and that environment variables are correctly defined)."

    def regex(self):
        return r"connection to server on socket \"(?P<socket>(.*))\" failed"


class DatabaseDoesNotExist:
    def title(self):
        return "The database ':database' is not created on the database server"

    def description(self):
        return "The application is trying to connect to the database ':database' but it looks like it has not been created."

    def regex(self):
        return r"database \"(?P<database>([\w\.]*))\" does not exist"


class DatabaseUserDoesNotExist:
    def title(self):
        return "The database user ':user' is not created on the database server"

    def description(self):
        return "The application is trying to connect with the user ':user' but it looks like it has not been created."

    def regex(self):
        return r"role \"(?P<user>([\w\.]*))\" does not exist"


class DivisionByZeroError:
    def title(self):
        return "Check variables for any values that could be 0"

    def description(self):
        return "Check any place you are doing division. You cannot divide by a zero."

    def regex(self):
        return r"division by zero"


class ContainerKeyNotFoundRegister:
    def title(self):
        return "Did you register the key in the service provider or Kernel?"

    def description(self):
        return (
            "Check the key name was correctly registered in a service provider or the Kernel file"
        )

    def regex(self):
        return r"key was not found in the container"


class ContainerKeyNotFoundServiceProvider:
    def title(self):
        return "Did you register the service provider?"

    def description(self):
        return "If you registered the key in your own service provider, did you register the provider in the config/providers.py file?"

    def regex(self):
        return r"key was not found in the container"

    def documentation_link(self):
        return "https://docs.masoniteproject.com/architecture/service-providers#registering-the-service-provider"


class NotFound404:
    def title(self):
        return "The '/:route' route could not be found"

    def description(self):
        return "Could not find the '/:route' route. Try checking spelling is correct and the '/:route' is registered correctly in your routes files. You can also run 'python craft routes:list' to make sure the route shows up correctly"

    def regex(self):
        return r"(?P<route>([\w]*)) \: 404 Not Found"


class ModelNotFound:
    def title(self):
        return "No record found when using find_or_fail()"

    def description(self):
        return """You probably used 'find_or_fail()' method on a Model, and no record has been found with the given primary key, a ModelNotFound exception has then been raised with a 404 error code.
        If you want this error to be silent you can use 'find()' method instead."""

    def regex(self):
        return r"No record found with the given primary key"


class DriverNotFound:
    def title(self):
        return "Driver Is Not Installed"

    def description(self):
        return ":package is required by the driver. You should install it with 'pip install :package' and refresh the page."

    def regex(self):
        return r"^Could not find the '(?P<package>([\w]*))' library"


class DatabaseDriverNotFound:
    def title(self):
        return "Database Driver Is Not Installed"

    def description(self):
        return ":package is required by the database driver. You should install it with 'pip install :package' and refresh the page."

    def regex(self):
        return r"^You must have the '(?P<package>([\w]*))' package installed"


class InvalidRouteMethodType:
    def title(self):
        return "The method type is incorrect"

    def description(self):
        return "If this is a GET route, check if the route is actually defined as Route.post(). Or the opposite"

    def regex(self):
        return r"(?P<route>([\w]*)) \: 404 Not Found"


class GetAttributeObject:
    def title(self):
        return "Check the class method exists"

    def description(self):
        return """
            Double check the object you are using and make sure it has the ':attribute' attribute.

            If you are using a builtin python type then check Python documentation.
            If you are using your own class then check the available methods.
            """

    def regex(self):
        return r"^'(?P<object>(\w+))' object has no attribute '(?P<attribute>(\w+))'"


class ModuleHasNoAttribute:
    def title(self):
        return "Check Class Import"

    def description(self):
        return """You might have expected to import the class when doing 'from :module import ...' but instead you have imported the module causing this AttributeError exception.

        Please check that the python module exports the class you want (e.g. through a __init__.py file) else you can write the import "from my.module.MyClass import MyClass"
        """

    def regex(self):
        return r"^module '(?P<module>(\w.+))' has no attribute 'find_or_fail'"


class ModuleNotCallable:
    def title(self):
        return "Check Class Import"

    def description(self):
        return """You might have expected to import the class when doing 'from :module import ...' but instead you have imported the module causing this TypeError exception when trying to instantiate the class.

        Please check that the python module exports the class you want (e.g. through a __init__.py file) else you can write the import "from my.module.MyClass import MyClass"
        """

    def regex(self):
        return r"'module' object is not callable"


class NoModuleNamed:
    def title(self):
        return "Module Not Found Error"

    def description(self):
        return "This is an import error. Check the file where you imported the ': module' module. Make sure its spelled right and make sure you pip installed this module correctly if this is supposed to come from a PYPI package."

    def regex(self):
        return r"No module named '(?P<module>(\w.+))'"


class Syntax:
    def title(self):
        return "Syntax Error"

    def description(self):
        return "Syntax errors are usually simple to fix. Just find the place that has invalid Python syntax and fix it. A good place to look is in your :class file on line :line"

    def regex(self):
        return r"^invalid syntax \((?P<class>(\w+\.py))+, line (?P<line>(\w+))"


class ImportIssue:
    def title(self):
        return "Import Issue"

    def description(self):
        return "This is an import error. Check the file where you imported the ':object' class and make sure it exists there."

    def regex(self):
        return r"^cannot import name '(?P<object>(\w+))'"


class Undefined:
    def title(self):
        return "Undefined Variable"

    def description(self):
        return "You are trying to use a variable that cannot be found. Check the ':variable' variable and see if it is declared, imported or in the correct scope depending on what the variable is."

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
            "You cannot call objects. The ':object' object has already been instantiated. "
            "Once an object is instantiated it cannot be called directly anymore. "
            "Check if the ':object' is instantiated already."
        )

    def regex(self):
        return r"^'(?P<object>(\w*))' object is not callable"


class SubscriptableIssue:
    def title(self):
        return "Object Not Subscriptable"

    def description(self):
        return "Looks like you expected ':object' to be an iterable but it is not. You can only use subscriptions, like x[0], on iterable type objects (like lists, dicts, and strings) but not ':object' in this case."

    def regex(self):
        return r"^'(?P<object>(\w+))' object is not subscriptable"


class StringIndicesMustBeIntegers:
    def title(self):
        return "Check Variable Type"

    def description(self):
        return (
            "This errors might occur when using subscriptions [] on an object. The most likely cause is that you expected the object to be a dict and wanted to access a key on it. "
            "Let's take the example of accessing 'some_key' on the dict named `my_var`: my_var['some_key'] will fail if 'my_var' happens to be a string ! You cannot access 'some_key' on it, you can only access indexes of the string with integers. "
            "Check that the variable is a dictionary and not a string."
        )

    def regex(self):
        return r"string indices must be integers"


class DjangoTemplateNotFound:
    def title(self):
        return "Check template exists in your apps 'templates' directory"

    def description(self):
        return "Check for a ':path' file inside the 'templates' directory of your app."

    def regex(self):
        return r"^(^(?P<path>(^(.+)\/([^\/]+)$)))"


class ContextShouldBeList:
    def title(self):
        return "Check the arguments to the template loader method."

    def description(self):
        return "Change the argument passed to the template loader from a list to a dictionary"

    def regex(self):
        return r"^context must be a dict rather than list"


class RenderArgumentsOutOfOrder:
    def title(self):
        return "Check the arguments to the template render method."

    def description(self):
        return "If trying to load a template, check the order of the arguments. The order should be (request, template, context). Context here is a dictionary."

    def regex(self):
        return r"^join\(\) argument must be str\, bytes\, or os.PathLike object\, not \'dict\'"
