import subprocess
from logging import getLogger
from os.path import exists, join
from os import makedirs
from airbox.process import run_command

logger = getLogger('airbox')

ROOT_MOUNT_POINT = '/mnt/airbox'
TARGET_DIR = '/mnt/aurora/data/'


def is_mount_point(dir_name):
    res = run_command(['mountpoint', dir_name, '-q'], can_ret_nonzero=True)
    return res.returncode == 0


def mount_dir(ip_or_hostname, mount_name, dest, passwd=None, **kwargs):
    if not exists(dest):
        makedirs(dest)
    if passwd is not None:
        kwargs['pass'] = passwd

    opts = ['{}={}'.format(k, kwargs[k]) for k in kwargs]
    mount_path = '//{}/{}'.format(ip_or_hostname, mount_name)

    logger.info('Attempting to create new mount: {} => {}'.format(ip_or_hostname, mount_name))
    run_command(['mount', mount_path, dest, '-o', ','.join(opts)])
    logger.info('Created mount point: ' + mount_path)


def run_instr_backup(instr, target_dir):
    """
    Runs the backups for a single instrument
    :param instr: A dictionary containing
    :param target_dir: The directory where the backup should be stored
    :return:
    """
    node = instr['node']

    # Ensure that the directory is mounted
    source = join(ROOT_MOUNT_POINT, instr['node']['name'], instr['mount_name']) + '/'
    dest = join(target_dir, instr['name'])
    if not is_mount_point(source):
        mount_dir(node['ip'], instr['mount_name'], source, user=node['user'], passwd=node['pass'])
        assert is_mount_point(source)

    logger.info('Backing up {} to {}'.format(source, dest))
    rsync_args = [
        '-ai',
        '--no-owner',
        '--no-group',
    ]

    command_args = ['rsync', *rsync_args, source, dest]
    run_command(command_args)
    subprocess.check_call(command_args)