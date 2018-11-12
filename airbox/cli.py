import argparse
import logging
import sys
from os import environ

from airbox import config
from airbox.backups import run_instr_backup
from airbox.commands import initialise_commands, run_command

logger = logging.getLogger('run_backups')


def process_args():
    parser = argparse.ArgumentParser(prog='airbox',
                                     description='A utility to help with the storage and backup of AirBox data')
    parser.add_argument('-c', '--config', help='Path to an AirBox configuration JSON file.',
                        default=environ.get('AIRBOX_CONFIG', None))
    parser.add_argument('-v', '--verbose', action='store_true', default=False)

    subparsers = parser.add_subparsers(dest='cmd')
    backup = subparsers.add_parser('backup', help='Perform a backup of all the airbox instruments')

    # Find and load all commands in airbox.commands
    initialise_commands(subparsers)

    return parser.parse_args()


def run_backup(args):
    failed_instr = []
    for i in config['instruments']:
        try:
            run_instr_backup(i, config['target'])
        except:
            logger.exception('An exception occured when backing up {}'.format(i['name']))
            failed_instr.append(i)
    if len(failed_instr):
        logger.error('{} instruments failed to backup. See log for more details'.format(len(failed_instr)))


def main():
    _args = process_args()
    logging.basicConfig(level=logging.DEBUG if _args.verbose else logging.INFO)

    if _args.config is None:
        logger.critical(
            'No configuration file specified. Use `--config` option or `AIRBOX_CONFIG` environment variable')
        sys.exit(1)
    config.load_config(_args.config)
    config.load_args(_args)

    if _args.cmd == 'backup':
        run_backup(_args)
    else:
        run_command()


if __name__ == '__main__':
    main()
