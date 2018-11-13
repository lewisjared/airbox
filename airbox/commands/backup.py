from logging import getLogger
from os import makedirs
from os.path import exists, join

from airbox import config
from airbox.process import run_command, FAILED_CMD_MSG
from .base import BaseCommand

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

    p = instr['path'] if 'path' in instr else ''
    rsync_args = [
        '-aiz',
        '--no-owner',
        '--no-group',
    ]

    if 'filter' in instr:
        rsync_args.extend([
            '--include="{}"'.format(instr['filter']),
            '--exclude="*"'
        ])

    command_args = ['rsync', *rsync_args, source + p, dest]
    res = run_command(command_args, can_ret_nonzero=True)
    if res.returncode != 0:
        logger.warning('rsync command returned non zero: {}'.format(res.args))
        can_ignore = check_rsync_stderr(res.stderr)
        if not can_ignore:
            logger.error(FAILED_CMD_MSG.format(res.stdout.decode(), res.stderr.decode()))
            raise OSError("Failed rsync command: {}".format(res.args))


def check_rsync_stderr(err):
    """
    Checks to see if the errors in the stderr of rsync are actual errors or can be ignored.
    :param err: stderr from an execution of rsync
    :return: True if errors can be ignored
    """
    res = True

    for l in err.split('\n'):
        if not len(l):
            continue
        if l.endswith('Device or resource busy (16)'):
            logger.warning(l)
            continue
        if l.startswith('rsync error: some files/attrs were not transferred'):
            continue
        return False
    return res


class BackupCommand(BaseCommand):
    name = 'backup'
    help = 'Perform a backup of all the airbox instruments'

    def run(self):
        failed_instr = []
        for i in config['instruments']:
            try:
                run_instr_backup(i, config['target'])
            except:
                logger.exception('An exception occured when backing up {}'.format(i['name']))
                failed_instr.append(i)
        if len(failed_instr):
            logger.error('{} instruments failed to backup. See log for more details'.format(len(failed_instr)))
