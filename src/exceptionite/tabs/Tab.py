class Tab:

    name = "Tab Name"
    icon = ""
    id = ""
    component = ""
    advertise_content = False

    def __init__(self, handler) -> None:
        self.handler = handler
        self.blocks = {}

    def add_block(self, block_class):
        block = block_class(self.handler)
        self.blocks.update({block.name: block})
        return self

    def configure(self):
        pass

    def get_block(self, name):
        return self.blocks.get(name)

    def serialize(self):
        self.configure()
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "component": self.component,
            "blocks": list(map(lambda b: b.serialize(), self.blocks.values())),
            "data": self.build(),
            "advertise_content": self.advertise_content,
            "has_content": self.has_content(),
        }

    def build(self):
        return {}

    def has_content(self):
        return any(
            list(map(lambda b: b.has_content(), self.blocks.values())),
        )
