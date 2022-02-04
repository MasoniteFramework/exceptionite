class Block:
    name = "Block Name"
    icon = "Icon Name"
    component = "KeyValBlock"

    def __init__(self, handler):
        self.handler = handler
        self.data = {}

    def serialize(self):
        self.data = self.build()
        return {
            "name": self.name,
            "icon": self.icon,
            "component": self.component,
            "data": self.data,
        }

    def build(self):
        raise NotImplementedError("block should implement build()")

    def has_content(self):
        return False
