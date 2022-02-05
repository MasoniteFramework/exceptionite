import os
from jinja2 import Environment, PackageLoader


class WebRenderer:
    def __init__(self, handler) -> None:
        self.handler = handler

    def render(self):
        path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "templates", "pyexceptions.js"
        )
        with open(path, "r") as f:
            script = f.read()

        env = Environment(loader=PackageLoader("exceptionite", "templates"))

        template = env.get_template("exception.html")
        return template.render({"data": self.handler.get_last_exception_data(), "script": script})

    # def render(self):
    #     path = os.path.dirname(os.path.dirname(__file__))
    #     file_loader = FileSystemLoader(os.path.join(path, "templates/"))
    #     env = Environment(loader=file_loader)
    #     template = env.get_template("exception.html")
    #     return template.render({"data": self.handler.get_last_exception_data()})
