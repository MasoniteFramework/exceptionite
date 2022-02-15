## Setting up this repository for development

To setup the package to get your package up and running, you should first take a look at `setup.py` and make any packages specific changes there. These include the classifiers and package name.

Then you should create a virtual environment and activate it

```
python3 -m venv venv
source venv/bin/activate
```

Then install from the requirements file

```
pip install -r requirements.txt
```

This will install `exceptionite` and development related packages.

## Running tests

```
python -m pytest
```
