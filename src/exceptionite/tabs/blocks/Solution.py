class SolutionsIntegration:

    name = "Possible Solutions"
    count = 0

    def __init__(self):
        self.registered_solutions = []
        self.register(
            DictionaryUpdateSequence(),
            ClassMethodExists(),
            GetAttributeObject(),
            GetAttributeController(),
            NoModuleNamed(),
            Syntax(),
            ImportIssue(),
            CSRFIssue(),
            Undefined(),
            WrongParameterCount(),
            WrongConstructorParameterCount(),
            ObjectNotCallable(),
            SubscriptableIssue(),
        )

    def content(self, handler):
        possible_solutions = []
        for solution in self.registered_solutions:
            r = re.compile(solution.regex())
            if r.match(handler.message()):
                description = solution.description()
                matches = [m.groupdict() for m in r.finditer(handler.message())]
                self.count += 1
                for code, replacement in matches[0].items():
                    description = description.replace(":" + code, replacement)

                solution.modified_description = description
                possible_solutions.append(solution)

        current_path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_path, "templates/solutions.html"), "r") as f:
            overflow_exception = f.read()

        loader = DictLoader(
            {
                "solutions.html": overflow_exception,
            }
        )

        environment = Environment(loader=loader, autoescape=select_autoescape(["html", "xml"]))
        return environment.get_template("solutions.html").render({"solutions": possible_solutions})

    def register(self, *solutions):
        self.registered_solutions += solutions
        return self
