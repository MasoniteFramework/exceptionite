import shlex
import subprocess

from ..Block import Block


class Git(Block):
    id = "git"
    name = "Git"
    icon = "ShareIcon"
    disable_scrubbing = True

    def build(self):
        git_version = subprocess.check_output(shlex.split("git --version")).strip()
        try:
            commit = subprocess.check_output(
                shlex.split("git rev-parse HEAD"), stderr=subprocess.STDOUT
            ).strip()
        except subprocess.CalledProcessError:
            # not a git repository
            return {
                "commit": "",
                "branch": "",
                "git_version": git_version.decode("utf-8"),
                "remote": "",
            }
        branch = subprocess.check_output(
            shlex.split("git rev-parse --abbrev-ref HEAD"), stderr=subprocess.STDOUT
        ).strip()
        try:
            remote = subprocess.check_output(
                shlex.split("git config --get remote.origin.url"), stderr=subprocess.STDOUT
            ).strip()
        except subprocess.CalledProcessError:
            remote = b""

        return {
            "commit": commit.decode("utf-8"),
            "branch": branch.decode("utf-8"),
            "git_version": git_version.decode("utf-8"),
            "remote": remote.decode("utf-8"),
        }

    def has_content(self):
        return True
