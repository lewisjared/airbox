import sys
from logging import getLogger
from os.path import abspath

from airbox import config
from .base import BaseCommand

logger = getLogger(__name__)

CRON_SCIPT = """# /etc/cron.d/airbox: crontab entries for the airbox package
# This was installed using the airbox cli tool: run `airbox install` again with a different configuration to change

5 * * * *   airbox    {python} {cli_script} --config {config_fname} run_schedule >> {log_file} 2>&1
"""


class InstallCommand(BaseCommand):
    """
    Takes the last 24 hours of spectronus data, decimates it and then emails the result to Dave Griffiths.
    """
    name = 'install'
    help = 'Install/update the scheduler'

    def initialise_parser(self, subparser):
        subparser.add_argument('--log-file',
                               help="Filename where the logs from the scheduler are written. This file is appended to "
                                    "on every invocation. This can include shell commands such as `date`. Defaults to "
                                    '/var/log/airbox_`date "+%%Y-%%m-%%d"`.log which creates a new file every day.',
                               default='/var/log/airbox/airbox_`date "+%Y-%m-%d"`.log')

    def run(self):
        out_fname = '/etc/cron.d/airbox'
        log_fname = config['log_file'].replace('%', '\\%')
        script = CRON_SCIPT.format(
            python=abspath(sys.executable),
            cli_script=abspath(sys.argv[0]),
            config_fname=abspath(config['config']),
            log_file=abspath(log_fname)
        )
        logger.info('Write the following lines to {}. Then ensure that {} is executable'.format(out_fname, out_fname))

        print(script)
