import importlib.metadata

from ..Block import Block


class Packages(Block):
    id = "packages"
    name = "Installed Packages"
    icon = "PuzzleIcon"
    disable_scrubbing = True

    def build(self):
        packages = {}
        for dist in importlib.metadata.distributions():
            packages.update({dist.metadata["Name"]: dist.version})
        return packages

    def has_content(self):
        return True
