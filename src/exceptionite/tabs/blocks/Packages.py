from re import A
import pkg_resources
import requests
import json
from json import loads

from .Block import Block


def get_latest_version(name):
    r = requests.get(f"https://pypi.org/pypi/{name}/json")
    if r.status_code == 200:
        version = r.json()["info"]["version"]
        return version
    return None


class Packages(Block):
    name = "Installed Packages"
    icon = "PuzzleIcon"

    def build(self):
        installed_packages = pkg_resources.working_set
        packages = {}
        # if self.handler.options.get("tabs.context.packages_update", False):
        #     with open(".pyexceptions.packages", "r+") as f:
        #         data = f.read()
        #         if data:
        #             versions = loads(data)
        #         else:
        #             versions = {}
        #         for package in installed_packages:
        #             latest_version = versions.get(package.project_name)
        #             if not latest_version:
        #                 latest_version = get_latest_version(package.project_name)
        #             versions[package.project_name] = latest_version
        #             packages.update(
        #                 {package.key: {"current": package.version, "latest": latest_version}}
        #             )
        #         json.dump(versions, f)
        # else:
        for package in installed_packages:
            packages.update({package.key: package.version})

        return packages
