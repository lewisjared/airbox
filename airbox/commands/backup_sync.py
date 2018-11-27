from logging import getLogger

from airbox import config
from airbox.process import run_command, FAILED_CMD_MSG
from .base import BaseCommand

logger = getLogger(__name__)


def run_backup(source, dest):
    """
    Backs up the shareddrive to 2 duplicate external harddrives

    After the voyage these harddrives are removed and replaced with new drives. One drive is returned to AAD to be
    copied to the data center and the other is returned to UoM.

    :param dest: The directory where to syncronise the data
    :return: The number of files modified/added by the rsync command
    """

    logger.info('Backing up {} to {}'.format(source, dest))

    rsync_args = [
        '-aiz',
        '--no-owner',
        '--no-group',
        '--no-perms',
        '--delete',
        '--exclude=plots',
        '--include=*.tar.gz',
        '--exclude=SP??????'
    ]

    command_args = ['rsync', *rsync_args, source, dest]
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


class BackupSyncCommand(BaseCommand):
    name = 'backup_sync'
    help = 'Syncronise the external harddrives with the shared drive'

    def run(self):
        run_backup(config['target'], config['backup_dirs'][0])
        run_backup(config['backup_dirs'][0], config['backup_dirs'][1])
