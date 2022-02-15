from dotty_dict import dotty
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from .Block import Block


class Tab:

    name = "Tab Name"
    icon = ""
    id = ""
    component = "BaseTab"
    advertise_content = False
    disable_scrubbing = False

    def __init__(self, handler) -> None:
        self.handler = handler
        self.blocks = {}
        tab_options = self.handler.options.get(f"handlers.{self.id}", {})
        self.options = dotty({} if isinstance(tab_options, bool) else tab_options)
        assert self.id, "Tab should declare an 'id' attribute !"

    def add_blocks(self, *block_classes: Type["Block"]):
        """Register the given block(s) in the tab."""
        for block_class in block_classes:
            block_options = self.options.get(block_class.id, {})
            block_options = dotty({} if isinstance(block_options, bool) else block_options)
            block = block_class(self, self.handler, block_options)
            self.blocks.update({block.id: block})
        return self

    def block(self, id):
        return self.blocks.get(id)

    def active_blocks(self):
        active_blocks = []
        display_tab = self.handler.options.get(f"handlers.{self.id}", True)
        if display_tab is False:
            return active_blocks
        elif display_tab is True:
            return self.blocks.values()

        for block in self.blocks.values():
            display_block = display_tab.get(block.id, True)
            if display_block is False:
                continue
            active_blocks.append(block)
        return active_blocks

    def serialize(self):
        raw_data = self.build()
        self.data = self.handler.scrub_data(raw_data, self.disable_scrubbing)
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "component": self.component,
            "blocks": list(map(lambda b: b.serialize(), self.active_blocks())),
            "data": self.data,
            "advertise_content": self.advertise_content,
            "has_content": self.has_content(),
        }

    def build(self):
        return {}

    def has_content(self):
        return any(
            list(map(lambda b: b.has_content(), self.active_blocks())),
        )
