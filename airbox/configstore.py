"""
Singleton for reading configuration from anywhere
"""

import json
import sys
from logging import getLogger
from os.path import abspath, exists

logger = getLogger(__name__)


class ConfigStore(object):
    """
    A container for holding onto configuration during the life of the program

    A call to `load_config` will read in the configuration from a JSON file. Afterwards, the configuration values can
    be accessed using the following:

    >>> from airbox import config
    >>> config['target_dir']
    """
    def __init__(self):
        self._config = {}
        self._config_loaded = False

    def __getitem__(self, item):
        if not self._config_loaded:
            raise ValueError('ConfigStore has not been loaded yet. `Call config.load_config`')
        try:
            return self._config[item]
        except KeyError:
            logger.warning('No config with key {}'.format(item))
            raise

    def load_config(self, config_fname):
        fname = abspath(config_fname)
        logger.info('Using configuration file: {}'.format(fname))
        if not exists(config_fname):
            logger.critical('Could not find config file ' + fname)
            sys.exit(1)

        config = json.load(open(fname))
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

        self._config_loaded = True
        self._config = config

        # Return the loaded configuration
        return config

    def load_args(self, args):
        """
        Reads a list of parsed command line arguments into the config.

        These values should override any values provided in a configuration file. This allows subparsers to specify
        additional configuration values which can be read in, while still allowing default values to exist in the
        static configuration file. The key where the configuration is stored is the same as the dest value specified
        when calling `parser.add_argument`
        :param args: Namespace from argparse
        """
        for k, v in args._get_kwargs():
            self._config[k] = v