"""
This module contains a number of other commands that can be run via the cli.

All classes in this submodule which inherit the baseclass `airbox.commands.base.Command` are automatically included in
the possible commands to execute via the commandline. The commands can be called using their `name` property.
"""

from logging import getLogger

from airbox import config
from .basic_plot import BasicPlotCommand
from .spectronus_subset import SpectronusSubsetCommand

logger = getLogger(__name__)

# Commands are registered below
_commands = [
    BasicPlotCommand(),
    SpectronusSubsetCommand()
]


def find_commands():
    """
    Finds all the Commands in this package
    :return: List of Classes within
    """
    # TODO: Make this actually do that. For now commands are manually registered
    pass


def initialise_commands(parser):
    """
    Initialise the parser with the commandline arguments for each parser
    :param parser:
    :return:
    """
    find_commands()
    for c in _commands:
        p = parser.add_parser(c.name, help=c.help)
        c.initialise_parser(p)


def run_command():
    """
    Attempts to run a command
    :param config: Configuration data
    :param args: Parsed commandline arguments from argparse
    """
    for c in _commands:
        if config['cmd'] == c.name:
            return c.run()
