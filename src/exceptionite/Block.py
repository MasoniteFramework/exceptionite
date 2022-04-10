class Block:
    id = ""
    name = "Block Name"
    icon = ""
    component = "BasicBlock"
    disable_scrubbing = False
    empty_msg = "No content."
    has_sections = False

    def __init__(self, tab, handler, options={}):
        # tab which holds the block
        self.tab = tab
        self.handler = handler
        self.options = options
        self.data = {}
        assert self.id, "Block should declare an 'id' attribute !"

    def serialize(self):
        raw_data = self.build()
        self.data = self.handler.scrub_data(raw_data, self.disable_scrubbing)
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "component": self.component,
            "data": self.data,
            "empty_msg": self.empty_msg,
            "has_content": self.has_content(),
            "has_sections": self.has_sections,
        }

    def build(self):
        raise NotImplementedError("block should implement build()")

    def has_content(self):
        return True
