import shlex
import subprocess
from weakref import CallableProxyType
from .Block import Block


class Git(Block):
    id = "git"
    name = "Git"
    icon = "ShareIcon"

    def build(self):
        # TODO: if no git repo
        # TODO: add config for remote name
        # return False

        git_version = subprocess.check_output(shlex.split("git --version")).strip()
        commit = subprocess.check_output(shlex.split("git rev-parse HEAD")).strip()
        branch = subprocess.check_output(shlex.split("git rev-parse --abbrev-ref HEAD")).strip()
        try:
            remote = subprocess.check_output(
                shlex.split("git config --get remote.origin.url")
            ).strip()
        except subprocess.CalledProcessError:
            remote = b""

        return {
            "commit": commit.decode("utf-8"),
            "branch": branch.decode("utf-8"),
            "git_version": git_version.decode("utf-8"),
            "remote": remote.decode("utf-8"),
        }
