import logging
import os
import sys

import yaml

from utils import print_bold_title, setup_cache, safe_copy

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()


def push(args):
    print_bold_title("Pushing local file to remote")

    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

        repo = setup_cache(config["cache"], config["repository"])
        _push_files(config["files"], repo)


def _push_files(files, repo):
    for file in files:
        logger.info(f"Processing {file}")

        local_file = os.path.expanduser(file)
        if os.path.exists(local_file):
            remote_file = repo.get_remote_filepath(local_file)
            logger.info(f"Writing contents of {local_file} to {remote_file}")
            safe_copy(local_file, remote_file)
        else:
            logger.warning(
                f"File {local_file} does not exist on this machine. Skipping"
            )

    # print the status of remote before commiting
    status = repo.status()

    if "working tree clean" in status:
        print_bold_title("No local changes to push.  Exiting.")
        return

    repo.commit_backup()
    repo.push()
