class Tab:

    name = "Tab Name"
    icon = ""
    id = ""
    component = "BaseTab"
    advertise_content = False

    def __init__(self, handler) -> None:
        self.handler = handler
        self.blocks = {}
        self.configure()

    def add_block(self, block_class):
        block = block_class(self.handler)
        self.blocks.update({block.id: block})
        return self

    def configure(self):
        return self

    def get_block(self, id):
        return self.blocks.get(id)

    def get_active_blocks(self):
        return [
            block
            for block in self.blocks.values()
            if self.handler.options.get("blocks").get(block.id, True)
        ]

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "component": self.component,
            "blocks": list(map(lambda b: b.serialize(), self.get_active_blocks())),
            "data": self.build(),
            "advertise_content": self.advertise_content,
            "has_content": self.has_content(),
        }

    def build(self):
        return {}

    def has_content(self):
        return any(
            list(map(lambda b: b.has_content(), self.get_active_blocks())),
        )
