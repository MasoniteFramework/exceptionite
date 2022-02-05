from .Tab import Tab
from .blocks.PackagesUpdates import PackagesUpdates


class RecommendationsTab(Tab):

    name = "Recommendations"
    id = "recommendations"
    icon = "CheckCircleIcon"
    advertise_content = True

    def configure(self):
        self.add_block(PackagesUpdates)
