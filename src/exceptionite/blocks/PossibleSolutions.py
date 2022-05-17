import re

import urllib.parse

from ..Block import Block
from .. import solutions


class PossibleSolutions(Block):

    id = "possible_solutions"
    name = "Possible Solutions"
    component = "PossibleSolutionsBlock"
    advertise_content = True
    disable_scrubbing = True
    empty_msg = "No solution found for this error."
    icon = "LightBulbIcon"

    def __init__(self, tab, handler, options):
        super().__init__(tab, handler, options)
        self.registered_solutions = []
        self.register(
            *solutions.PythonSolutions.get(),
        )

    def build(self):
        possible_solutions = []
        for solution in self.registered_solutions:
            r = re.compile(solution.regex())
            doc_link = None
            if r.search(self.handler.message()):
                description = solution.description()
                title = solution.title()
                matches = [m.groupdict() for m in r.finditer(self.handler.message())]
                if hasattr(solution, "documentation_link"):
                    if solution.documentation_link():
                        doc_link = solution.documentation_link()
                for code, replacement in matches[0].items():
                    description = description.replace(":" + code, replacement)
                    title = title.replace(":" + code, replacement)

                possible_solutions.append(
                    {"title": title, "description": description, "doc_link": doc_link}
                )

        # build request_link
        request_link = ""
        if not possible_solutions:
            request_link = self.get_request_link()

        return {
            "first": possible_solutions[0] if len(possible_solutions) > 0 else None,
            "solutions": possible_solutions,
            "request_link": request_link,
        }

    def get_request_link(self):
        params = {
            "title": f"Add exceptionite solution for `{self.handler.exception()}`",
            "body": f"A solution is missing:\nException namespace: `{self.handler.namespace()}`\nError message:\n```\n{self.handler.message()}\n```",  # noqa: E501
            "labels": "solution-request",
        }
        return f"https://github.com/MasoniteFramework/exceptionite/issues/new/?{urllib.parse.urlencode(params)}"  # noqa: E501

    def register(self, *solutions):
        self.registered_solutions += solutions
        return self

    def has_content(self):
        return len(self.data.get("solutions")) > 0
