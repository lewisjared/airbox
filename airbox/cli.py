import argparse
import json
import logging
import sys
from os import environ
from os.path import exists

from airbox.backups import run_instr_backup

logger = logging.Logger('run_backups')


def load_config(config_fname):
    if config_fname is None:
        logger.critical(
            'No configuration file specified. Use `--config` option or `AIRBOX_CONFIG` environment variable')
        sys.exit(1)

    if not exists(config_fname):
        logger.critical('Could not find config file ' + config_fname)
        sys.exit(1)

    config = json.load(open(config_fname))
    assert 'nodes' in config
    assert 'instruments' in config

    def find_node(node_name):
        for n in config['nodes']:
            if n['name'] == node_name:
                return n
        raise ValueError('Could not find configuration for node: "{}"'.format(node_name))

    # Flatten instruments.node
    for instr in config['instruments']:
        assert 'node' in instr
        instr['node'] = find_node(instr['node'])

    return config


def process_args():
    parser = argparse.ArgumentParser(prog='airbox',
                                     description='A utility to help with the storage and backup of AirBox data')
    parser.add_argument('-c', '--config', help='Path to an AirBox configuration JSON file.',
                        default=environ.get('AIRBOX_CONFIG', None))
    parser.add_argument('-v', '--verbose', action='store_true', default=False)

    subparsers = parser.add_subparsers(dest='cmd')
    backup = subparsers.add_parser('backup', help='Perform a backup of all the airbox instruments')

    return parser.parse_args()


def run_backup(config, args):
    for i in config['instruments']:
        run_instr_backup(i, config['target'])


def main():
    _args = process_args()
    logging.basicConfig(level=logging.DEBUG if _args.verbose else logging.INFO)

    config = load_config(_args.config)

    if _args.cmd == 'backup':
        run_backup(config, _args)


if __name__ == '__main__':
    main()
