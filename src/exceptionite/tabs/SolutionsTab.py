from .Tab import Tab
from .blocks.StackOverflow import StackOverflow
from .blocks.PossibleSolutions import PossibleSolutions


class SolutionsTab(Tab):

    name = "Solutions"
    id = "solutions"
    icon = "LightBulbIcon"
    advertise_content = True

    def configure(self):
        self.add_block(PossibleSolutions)
        self.add_block(StackOverflow)
