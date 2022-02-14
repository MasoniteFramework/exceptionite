import re

from .Block import Block
from ..solutions import default


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
            default.DictionaryUpdateSequence(),
            default.ClassMethodExists(),
            default.GetAttributeObject(),
            default.NoModuleNamed(),
            default.Syntax(),
            default.ImportIssue(),
            default.Undefined(),
            default.WrongParameterCount(),
            default.WrongConstructorParameterCount(),
            default.ObjectNotCallable(),
            default.SubscriptableIssue(),
        )

    def build(self):
        possible_solutions = []
        for solution in self.registered_solutions:
            r = re.compile(solution.regex())
            if r.match(self.handler.message()):
                description = solution.description()
                matches = [m.groupdict() for m in r.finditer(self.handler.message())]
                for code, replacement in matches[0].items():
                    description = description.replace(":" + code, replacement)

                possible_solutions.append({"title": solution.title(), "description": description})

        return {
            "first": possible_solutions[0] if len(possible_solutions) > 0 else None,
            "solutions": possible_solutions,
        }

    def register(self, *solutions):
        self.registered_solutions += solutions
        return self

    def has_content(self):
        return len(self.data.get("solutions")) > 0
