import argparse
import logging
import sys
from os import environ

from airbox import config
from airbox.commands import initialise_commands, run_command

logger = logging.getLogger('airbox')


def process_args():
    parser = argparse.ArgumentParser(prog='airbox',
                                     description='A utility to help with the storage and backup of AirBox data')
    parser.add_argument('-c', '--config', help='Path to an AirBox configuration JSON file. The location of this file '
                                               'can also be specified using the "AIRBOX_CONFIG" environment variable.',
                        default=environ.get('AIRBOX_CONFIG', None))
    parser.add_argument('-v', '--verbose', action='store_true', default=False)
    parser.add_argument('--debug', action='store_true', default=False, help="Enable debug mode which disables sending "
                                                                            "of emails")

    subparsers = parser.add_subparsers(dest='cmd')

    # Find and load all commands in airbox.commands
    initialise_commands(subparsers)

    return parser.parse_args()


def main():
    _args = process_args()
    logging.basicConfig(level=logging.DEBUG if _args.verbose else logging.INFO,
                        format="%(asctime)s %(levelname)s:%(name)s:%(message)s")

    if _args.config is None:
        logger.critical(
            'No configuration file specified. Use `--config` option or `AIRBOX_CONFIG` environment variable')
        sys.exit(1)
    config.load_config(_args.config)
    config.load_args(_args)

    run_command(config['cmd'])


if __name__ == '__main__':
    main()
