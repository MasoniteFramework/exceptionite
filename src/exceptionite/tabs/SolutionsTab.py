from ..Tab import Tab
from ..blocks.StackOverflow import StackOverflow
from ..blocks.PossibleSolutions import PossibleSolutions


class SolutionsTab(Tab):

    name = "Solutions"
    id = "solutions"
    icon = "LightBulbIcon"
    advertise_content = True

    def __init__(self, handler):
        super().__init__(handler)
        self.add_blocks(PossibleSolutions, StackOverflow)
