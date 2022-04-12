import re

from attr import has

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
            solutions.DictionaryUpdateSequence(),
            solutions.DictionaryUpdateSequenceWithList(),
            solutions.UnsupportedOperand(),
            solutions.ContainerKeyNotFoundServiceProvider(),
            solutions.ContainerKeyNotFoundRegister(),
            solutions.ClassMethodExists(),
            solutions.ClassModelMethodExists(),
            solutions.ImportIssueWithController(),
            solutions.IncorrectControllerName(),
            solutions.IncorrectlyDefinedRoute(),
            solutions.RouteNameNotFound(),
            solutions.IncludedTemplateNotFound(),
            solutions.UnexpectedEndBlock(),            
            solutions.QueryDefaultValue(),
            solutions.NoColumnExistsOnWhere(),
            solutions.NoColumnExistsOnWhereSQLite(),
            solutions.NoColumnExistsOnSelect(),
            solutions.GetAttributeObject(),
            solutions.NoModuleNamed(),
            solutions.Syntax(),
            solutions.ImportIssue(),
            solutions.Undefined(),
            solutions.WrongParameterCount(),
            solutions.WrongConstructorParameterCount(),
            solutions.ObjectNotCallable(),
            solutions.SubscriptableIssue(),
            solutions.NotFound404(),
            solutions.InvalidRouteMethodType(),
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

                possible_solutions.append({"title": title, "description": description, "doc_link": doc_link})

        return {
            "first": possible_solutions[0] if len(possible_solutions) > 0 else None,
            "solutions": possible_solutions,
        }

    def register(self, *solutions):
        self.registered_solutions += solutions
        return self

    def has_content(self):
        return len(self.data.get("solutions")) > 0
