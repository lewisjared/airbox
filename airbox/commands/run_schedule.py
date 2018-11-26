from datetime import datetime
from logging import getLogger
import sys

from airbox import config
from airbox.mail import sendmail
from .base import BaseCommand

logger = getLogger(__name__)


def should_run(sch):
    f = sch['frequency']
    t = datetime.utcnow().time()
    if f.upper() == 'D':
        # Run daily jobs if called before 0100
        return t.hour == 0
    elif f.upper() == 'H':
        # Cron job is scheduled to run every hour
        return True
    else:
        logger.error('Invalid frequency argument ({}) for command ({})'.format(f, f['command']))


class RunScheduleCommand(BaseCommand):
    """
    Takes the last 24 hours of spectronus data, decimates it and then emails the result to Dave Griffiths.
    """
    name = 'run_schedule'
    help = 'Run the scheduler. This runs the tasks that need to be run daily or every hour'

    def run(self):
        # Late importing to resolve circular dependency
        from airbox.commands import run_command
        schedules = config['schedule']

        _config = config._config
        for s in schedules:
            if not should_run(s):
                logger.info('Skipping command: {}'.format(s['command']))
                continue

            # Run the command
            logger.info('Running command: {}'.format(s['command']))
            try:
                config._config = _config.copy()
                if 'args' in s:
                    config._config.update(s['args'])
                run_command(s['command'])
            except:
                exc_info = sys.exc_info()
                logger.exception('Command failed. Emailing expeds')
                sendmail(config['email_expeditioners'], "Scheduled command failed: {}".format(s['command']),
                         "{}. Check the airbox log (typically in /var/log/airbox/) on the airbox server for more "
                         "information.".format(exc_info[1]))
