import pkg_resources

from ..Block import Block


class Packages(Block):
    id = "packages"
    name = "Installed Packages"
    icon = "PuzzleIcon"
    disable_scrubbing = True

    def build(self):
        packages = {}
        for package in pkg_resources.working_set:
            packages.update({package.key: package.version})
        return packages

    def has_content(self):
        return True
