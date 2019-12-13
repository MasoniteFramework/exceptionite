
<p align="center">
<img src="https://i.imgur.com/rEXcoMn.png" width="160px"> 
</p>

# Introduction

**Using this library does not require Masonite.**

This library is a way to easily interact with exception classes. You can easily pass in an exception into the `Handler` class (usage docs below) and you can get so much information from the exception in an elegant fashion.

You can even render it into a beautiful HTML exception page. 

## Learning Masonite

Masonite strives to have extremely comprehensive documentation. All documentation can be [Found Here](https://masoniteframework.gitbooks.io/docs/content/) and would be wise to go through the tutorials there. If you find any discrepencies or anything that doesn't make sense, be sure to comment directly on the documentation to start a discussion!

Also be sure to join the [Slack channel](https://masoniteframework.gitbooks.io/docs/content/)!

## Setting up this repository for development

To setup the package to get your package up and running, you should first take a look at `setup.py` and make any packages specific changes there. These include the classifiers and package name.

Then you should create a virtual environment and activate it

```
$ python3 -m venv venv
$ source venv/bin/activate
```

Then install from the requirements file

```
$ pip install -r requirements.txt
```

This will install Masonite and a few development related packages like pytest.

Finally you can run the tests and start building your application.

```
$ python -m pytest
```

# Usage

In order to use this class you will first need to install it:

```
$ pip install masonite-errors
```

## Usage for Masonite

If you are installing this library in your Masonite application you can simply add the Service Provider to your `config/providers.py` file:

```python
from masonite.errors.providers import ErrorProvider

PROVIDERS = [
    # ...
    ErrorProvider,
]
```

You will now have a beautiful new exception screen!

## Usage Outside of Masonite

If you are not using Masonite you can still use this library. You can import the `Handler` class. This is the main exception handler class. This class accepts an exception. Here is an example of how to use it:

```python
from masonite.errors import Handler

try:
    2/0
except Exception as e:
    handler = Handler(e)
```

Once you have the handler class theres a whole bunch of things we can now do!

## Getting Exception Values:

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

You can render an elegant exception page by calling the `render` method:

```python
handler.render() #== <html> ... </html>
```

If you have a framework or an application you can swap the exception handler out with then this is a great method to use.

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