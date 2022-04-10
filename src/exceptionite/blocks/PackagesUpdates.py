import pkg_resources
import requests

from ..Block import Block


def get_latest_version(name):
    r = requests.get(f"https://pypi.org/pypi/{name}/json")
    if r.status_code == 200:
        version = r.json()["info"]["version"]
        return version
    return None


class PackagesUpdates(Block):
    id = "packages_updates"
    name = "Packages to update"
    icon = "ArrowCircleUpIcon"
    component = "PackagesUpdatesBlock"
    empty_msg = "Selected packages are up to date !"
    disable_scrubbing = True

    def build(self):
        installed_packages = {
            package.key: package.version for package in pkg_resources.working_set
        }

        packages_to_check = self.options.get("list", ["exceptionite"])
        packages = {}
        if packages_to_check:
            for package_name in packages_to_check:
                current_version = installed_packages.get(package_name)
                latest_version = get_latest_version(package_name)
                if current_version != latest_version:
                    packages.update(
                        {
                            package_name: {
                                "current": installed_packages.get(package_name),
                                "latest": latest_version,
                            }
                        }
                    )

        return packages

    def has_content(self):
        return len(self.data.keys()) > 0
