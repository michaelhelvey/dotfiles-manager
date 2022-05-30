"""
Michael's Personal Dotfiles CLI
"""

import argparse

from fetch import fetch
from push import push

def main() -> int:
    parser = argparse.ArgumentParser(description="Personal dotfiles CLI")
    sub = parser.add_subparsers(help='sub-command help')

    sync_parser = sub.add_parser('sync', help='Sync files from remote to local')
    sync_parser.set_defaults(function=fetch)

    push_parser = sub.add_parser('push', help='Push file from local to remote')
    push_parser.set_defaults(function=push)

    args = parser.parse_args()
    args.function(args)

    return 0


if __name__ == "__main__":
    exit(main())
