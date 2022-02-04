from .Tab import Tab
from .blocks.Environment import Environment
from .blocks.Packages import Packages
from .blocks.Git import Git


class ContextTab(Tab):

    name = "Context"
    id = "context"
    icon = "ViewListIcon"
    component = "ContextTab"

    def configure(self):
        self.add_block(Environment)
        self.add_block(Packages)
        self.add_block(Git)
