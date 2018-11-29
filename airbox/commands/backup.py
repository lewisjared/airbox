from logging import getLogger
from os import makedirs
from os.path import join, exists

from airbox import config
from airbox.dir import get_instr_dir
from airbox.process import run_command, FAILED_CMD_MSG
from .base import BaseCommand

logger = getLogger(__name__)

ROOT_MOUNT_POINT = '/mnt/airbox'


def is_mount_point(dir_name):
    res = run_command(['mountpoint', dir_name, '-q'], can_ret_nonzero=True)
    return res.returncode == 0


def run_instr_backup(instr):
    """
    Runs the backups for a single instrument

    :param instr: A dictionary containing
    :return: The number of files modified/added by the rsync command
    """
    source = join(ROOT_MOUNT_POINT, instr['node']['name'], instr['mount_name']) + '/'
    dest = get_instr_dir(instr['name'])

    if not exists(dest):
        makedirs(dest)

    assert is_mount_point(source)

    logger.info('Backing up {} to {}'.format(source, dest))

    p = instr['path'] if 'path' in instr else ''
    rsync_args = [
        '-aiz',
        '--no-owner',
        '--no-group',
    ]

    # Add in extra args
    if 'extra' in instr:
        rsync_args.extend(instr['extra'].split())

    if 'filter' in instr:
        rsync_args.extend([
            '--include={}'.format(instr['filter']),
            '--exclude=*'
        ])

    command_args = ['rsync', *rsync_args, source + p, dest]
    res = run_command(command_args, can_ret_nonzero=True)

    if res.returncode != 0:
        logger.warning('rsync command returned non zero: {}'.format(res.args))
        can_ignore = check_rsync_stderr(res.stderr.decode())
        if not can_ignore:
            logger.error(FAILED_CMD_MSG.format(res.stdout.decode(), res.stderr.decode()))
            raise OSError("Failed rsync command: {}".format(res.args))

    # Count the number of lines in STDOUT - this corresponds to the number of files added/modified
    num_files_modified = len(res.stdout.decode().split('\n'))
    logger.info('{} files added or modified'.format(num_files_modified))

    return num_files_modified


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
                num_files = run_instr_backup(i)
                if num_files == 0:
                    logger.error('No files backed up. Marking instrument as failed')
                    failed_instr.append(i)
            except:
                logger.exception('An exception occured when backing up {}'.format(i['name']))
                failed_instr.append(i)
        if len(failed_instr):
            # Raise an exception so an email will be sent any instruments fail to backup
            logger.error('{} instruments failed to backup. See log for more details'.format(len(failed_instr)))
            raise ValueError('{} instruments failed to backup'.format(len(failed_instr)))
