from os import makedirs
from os.path import join, exists

from airbox import config


def get_plot_dir():
    """
    Get the directory where plots created for the voyage are saved

    If this directory doesn't exist it is created.
    :return: directory
    """
    d = join(config['target'], 'plots')
    if not exists(d):
        makedirs(d)
    return d


def get_backup_dir():
    return join(config['target'], 'raw')


def get_instr_dir(instr_name):
    return join(get_backup_dir(), instr_name)
