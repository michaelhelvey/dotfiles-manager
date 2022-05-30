import logging
import os
import subprocess as sb
import sys

import yaml
from termcolor import colored

from utils import print_bold_title, setup_cache, compare_files, ask_user, safe_copy

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()


def fetch(args):
    print_bold_title("Syncing local files with remote")

    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

        repo = setup_cache(config["cache"], config["repository"])
        _sync_files(config["files"], repo)


def _sync_files(files, repo):
    for file in files:
        logger.info(f"Processing {file}")

        local_file = os.path.expanduser(file)

        remote_file = repo.get_remote_filepath(local_file)
        if not os.path.exists(local_file):
            logger.info(f"Creating new file {local_file}")
            safe_copy(remote_file, local_file)
            continue

        if not compare_files(local_file, remote_file):
            print(
                colored(
                    f"Error: files are not the same: {local_file} {remote_file}",
                    "yellow",
                    attrs=["bold"],
                )
            )
            sb.call(["diff", local_file, remote_file])

            overwrite = ask_user(
                "Overwrite this file?", on_failure=lambda: logger.info("Skipping file")
            )
            if overwrite:
                logger.info(f"Writing contents of {remote_file} to {local_file}")
                safe_copy(remote_file, local_file)

    print_bold_title("Sync complete.  Local files are now identical to remote")
