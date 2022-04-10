from ..Tab import Tab
from ..blocks.Environment import Environment
from ..blocks.Packages import Packages
from ..blocks.Git import Git


class ContextTab(Tab):

    name = "Context"
    id = "context"
    icon = "ViewListIcon"

    def __init__(self, handler):
        super().__init__(handler)
        self.add_blocks(Environment, Packages, Git)
