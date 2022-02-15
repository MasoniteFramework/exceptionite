
# Exceptionite

<p align="center">
  <img alt="GitHub Workflow Status (branch)" src="https://img.shields.io/github/workflow/status/MasoniteFramework/exceptionite/Test%20Application/2.0-dev">
  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="Python Version">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/exceptionite">
  <img alt="License" src="https://img.shields.io/github/license/MasoniteFramework/exceptionite">
  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

A Python exception library designed to make handling and displaying exceptions a cinch.

You can even render it into a beautiful HTML exception page!

![](screenshots/masonite_1.png)
![](screenshots/masonite_2.png)

Or render it to your terminal:

![](screenshots/terminal_handler.png)

# Getting Started

First install the package:

```bash
pip install exceptionite
```

Then you can follow instruction for your use case:

- [Masonite](#usage-for-masonite)
- [Flask](#usage-for-flask)
- [Django](#usage-for-django)
- [Basic Python](#usage-for-python)

## Usage for Masonite

Masonite 4 is already using `exceptionite` for its default error page so you don't have anything
to set up.
If you are using `Masonite < 4.0`, please use `exceptionite < 2.0`.

## Usage for Flask

If you are using `Flask` you can also use this package! Here is an example for a flask application:

```python
from flask import Flask, request
from exceptionite import Handler, Block

app = Flask(__name__)
handler = Handler()

class FlaskContextBlock(Block):
    id = "flask"
    name = "Flask"
    icon = "DesktopComputerIcon"

    def build(self):
        return {
            "Path": request.path,
            "Input": dict(request.args),
            "Request Method": request.method,
        }

handler.renderer("web").tab("context").add_blocks(FlaskContextBlock)


@app.errorhandler(Exception)
def handle_exception(e):
    handler.start(e)
    return handler.render("web")


@app.route('/<world>')
def hello(world):
    test = 'Hello World'
    return 2/0


if __name__ == '__main__':
    app.run(debug=True)
```

You'll now see this beautiful exception page:
![](screenshots/flask_1.png)
![](screenshots/flask_2.png)


## Usage for Django

You can customize error reports in Django in `DEBUG` mode as explained in the [docs](https://docs.djangoproject.com/en/3.2/howto/error-reporting/#custom-error-reports).
You need to write a custom `ExceptionReporter`:

```python
# settings.py
DEFAULT_EXCEPTION_REPORTER = "my_app.handler.ExceptioniteReporter"

# my_app/handler.py
from exceptionite import Handler

handler = Handler()

class ExceptioniteReporter:

    def __init__(self, request, exc_type, exc_value, tb):
        self.request = request
        self.exception = exc_value

    def get_traceback_html(self):
        handler.start(self.exception)
        handler.render("terminal")
        return handler.render("web")
```


## Usage for Python

If you are not using a specific framework you can still use this library. You just have to get
an instance of the `Handler` class and use the `start()` method to start handling the exception.

Then you can get useful information easily and also define how you want to render the error. You
can even add your own renderer.

```python
from exceptionite import Handler

try:
    2/0
except Exception as e:
    handler = Handler()
    handler.start(e)
```

Once you have the handler class theres a whole bunch of things we can now do!

### Getting Exception Details

Getting the exception name:

```python
handler.exception() #== ZeroDivisionError
```

Getting the exception message:

```python
handler.message() #== cannot divide by 0
```

Getting the exception namespace:

```python
handler.namespace() #== builtins.ZeroDivisionError
```

## Getting Environment Specific Information:

Getting the Python version:

```python
handler.python_version #== 3.6.5
```

Getting the default encoding:

```python
handler.default_encoding #== utf-8
```

Getting the file system encoding:

```python
handler.file_system_encoding #== utf-8
```

Getting the platform:

```python
handler.platform #== windows
```

## Rendering an HTML page

You can render an elegant exception page by using the `render` method with the `WebRenderer`:

```python
handler.render("web") #== <html> ... </html>
```

If you have a framework or an application you can swap the exception handler out with this handler
and then call this method.

## Contexts

Sometimes you will need to add more information to the exception page. This is where contexts come into play. Contexts are the ability to add any information you need to help you debug information.

If you use a framework like Masonite you might want to see information related to your Service Providers. If you use a framework like django you might want to see a list of your installed apps.

On the right side of the HTML page you will see a section of information. These are where the contexts are diplayed.

You can register new contexts by supplied a dictionary of the context name and a dictionary of the key value pairs:

```python
import sys

handler.context({
    'System Variables': {
        'sys argv': sys.argv
    }
})
```

Now this information will be displayed on the right hand side of the exception page.


<img width="1435" alt="Screen Shot 2019-12-15 at 11 49 39 AM" src="https://user-images.githubusercontent.com/20172538/70866053-b1cc3f00-1f32-11ea-9d4f-33805b16ecde.png">


# Contributing

Please read the [Contributing Documentation](CONTRIBUTING.md) here.

# Maintainers

- [Joseph Mancuso](https://github.com/josephmancuso)
- [Samuel Girardin](https://www.github.com/girardinsamuel)

# License

Exceptionite is open-sourced software licensed under the [MIT license](LICENSE).
