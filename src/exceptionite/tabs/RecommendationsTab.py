from ..Tab import Tab
from ..blocks.PackagesUpdates import PackagesUpdates


class RecommendationsTab(Tab):

    name = "Recommendations"
    id = "recommendations"
    icon = "CheckCircleIcon"
    advertise_content = True

    def __init__(self, handler):
        super().__init__(handler)
        self.add_blocks(PackagesUpdates)
