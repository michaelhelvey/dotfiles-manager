import filecmp
import os
import platform
import sys
import shutil

from termcolor import colored

from git import GitRepo


def print_bold_title(message: str):
    print(colored(f">>> {message}", attrs=["bold"]))


def get_hostname() -> str:
    if platform.system() == "Windows":
        return platform.uname().node
    else:
        return os.uname()[1]


def ask_user(prompt, on_failure=None):
    answer = input(f"> {prompt} (y/n): ")

    accepted_inputs = ["Y", "y", "yes", "Yes"]
    if answer in accepted_inputs:
        return True
    else:
        if on_failure:
            on_failure()
        return False


def compare_files(src, dst):
    # because this is shallow, you could obviously break it, but presumably you
    # won't try to do that :)
    return filecmp.cmp(src, dst, shallow=True)


def setup_cache(cache_dir: str, repository: str):
    """
    Create various needed files and directories.
    """
    cache_dir = os.path.abspath(os.path.expanduser(cache_dir))
    if not os.path.exists(cache_dir):
        print(f"local cache does not exist.  Creating directory at {cache_dir}")
        os.makedirs(cache_dir)

    git_dir = os.path.join(cache_dir, "repo")
    repo = GitRepo.clone(repository, git_dir)

    hostname = get_hostname()
    branch_exists = repo.checkout(hostname)

    def handle_user_quit():
        print(
            colored(
                f"Exiting sync job because use requested new config files for machine not be created based on master",
                "red",
                attrs=["bold"],
            )
        )
        sys.exit(1)

    if not branch_exists and ask_user(
        f"Configs for host {hostname} do not exist.  Create based on master?",
        on_failure=handle_user_quit,
    ):
        repo.create_branch(hostname)

    # once we know that we're on the latest branch, pull in the latest changes.
    # At this point, we're all set up to do whatever we need to do (push local
    # changes, propagate remote changes, etc)
    repo.update_current_branch()

    return repo


def safe_copy(src, dst):
    dir = os.path.dirname(dst)
    if not os.path.exists(dir):
        os.makedirs(dir)

    shutil.copy(src, dst, follow_symlinks=True)
