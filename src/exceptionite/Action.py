class Action:
    name = "Action Name"
    icon = ""
    id = ""
    component = ""

    def __init__(self, handler) -> None:
        self.handler = handler

    def run(self, options={}):
        # do something
        return "Action executed !"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "component": self.component,
        }
