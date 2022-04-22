import os
from setuptools import setup

meta = {}
with open(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), "src", "exceptionite", "version.py"),
    "r",
) as f:
    exec(f.read(), meta)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="exceptionite",
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=meta["__version__"],
    description="Exception Handling Made Easy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    # The project's main homepage.
    url="https://github.com/masoniteframework/exceptionite",
    # Author details
    author="The Masonite Community",
    author_email="joe@masoniteproject.com",
    # Choose your license
    license="MIT license",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 5 - Production/Stable",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Environment :: Web Environment",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        # List package on masonite packages website
        "Framework :: Masonite",
    ],
    # What does your project relate to?
    keywords="Masonite, Python, Development, Framework",
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    package_dir={"": "src"},
    packages=[
        "exceptionite",
        "exceptionite.blocks",
        "exceptionite.renderers",
        "exceptionite.tabs",
        "exceptionite.django",
    ],
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=["jinja2", "requests", "colorama", "dotty-dict", "typing-extensions", "mock"],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[test]
    extras_require={
        "test": [
            "black",
            "flake8",
            "coverage",
            "pytest",
            "pytest-cov",
            "twine>=1.5.0",
            "wheel",
        ],
    },
)
