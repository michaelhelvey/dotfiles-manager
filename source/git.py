from __future__ import annotations

from datetime import datetime
import logging
import os
import subprocess as sb
import sys
import pathlib
from typing import Optional

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()


class GitRepo:
    def __init__(self, cwd: str):
        self.cwd = cwd

    @staticmethod
    def clone(repo: str, dst: Optional[str] = None) -> GitRepo:
        """
        Creates a new repository in a given directory.  If the repository is
        already present in that directory, then simply fetches origin.
        """
        if not dst:
            dst = _find_repo_pathname(repo)

        dst = os.path.abspath(dst)

        repo_exists = os.path.exists(os.path.join(dst, ".git"))
        if not repo_exists:
            logger.info(f"Repo does not exist at {dst}.  Cloning fresh repository")
            sb.check_call(["git", "clone", repo, dst])
        else:
            logger.info(f"Repo already exists at {dst}.  Fetching origin")
            sb.check_call(["git", "fetch", "origin"], cwd=dst)

        return GitRepo(dst)

    @property
    def current_branch(self) -> str:
        return (
            sb.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=self.cwd)
            .decode()
            .strip()
        )

    def checkout(self, branch_name: str) -> bool:
        """
        Tries to checkout a branch, and returns whether the branch exists not not.
        """
        logger.info(f"Checking out branch {branch_name}")
        return sb.call(["git", "checkout", branch_name], cwd=self.cwd) == 0

    def create_branch(self, branch_name: str):
        logger.info(f"Creating branch {branch_name}")
        sb.check_call(["git", "checkout", "-b", branch_name], cwd=self.cwd)

    def pull(self):
        logger.info("Pulling current branch")
        sb.check_call(["git", "pull", "origin", self.current_branch], cwd=self.cwd)

    def push(self):
        logger.info("Pushing current branch to remote")
        sb.check_call(["git", "push", "origin", self.current_branch], cwd=self.cwd)

    def update_current_branch(self):
        branch = self.current_branch
        logger.info(
            f"Pulling latest changes into current branch (strategy=merge, branch={branch})"
        )
        sb.check_call(["git", "merge", f"origin/{branch}"], cwd=self.cwd)

    def get_remote_filepath(self, file: str):
        path = os.path.expanduser(file)

        if os.path.isdir(path):
            return os.path.join(self.cwd, path)
        else:
            parent = pathlib.Path(path).parts[-2]
            return os.path.join(self.cwd, parent, os.path.basename(file))

    def status(self) -> str:
        return sb.check_output(["git", "status"], cwd=self.cwd).decode()

    def commit_backup(self):
        dt = datetime.now()
        msg = f"Backup {dt.strftime('%D %T %p')}"
        logger.info(
            f"Committing changes with message '{msg}' on branch {self.current_branch}"
        )
        sb.check_output(["git", "add", "."], cwd=self.cwd)
        sb.check_output(["git", "commit", "-m", msg], cwd=self.cwd)


def _find_repo_pathname(repo: str) -> str:
    basename = os.path.basename(repo)

    if basename.endswith(".git"):
        basename = basename.replace(".git", "")

    return basename
