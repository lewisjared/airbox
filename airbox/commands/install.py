from logging import getLogger

import sys
from os import chmod
from os.path import abspath
from airbox import config
from .base import BaseCommand

logger = getLogger(__name__)


CRON_SCIPT = """#!/bin/sh

# Cron job for automatically running the backups for AirBox
# This was installed using the airbox cli tool

{python} {cli_script} --config {config_fname} backup >> {log_file}"""


class InstallCommand(BaseCommand):
    """
    Takes the last 24 hours of spectronus data, decimates it and then emails the result to Dave Griffiths.
    """
    name = 'install'
    help = 'Install/update the scheduler'

    def initialise_parser(self, subparser):
        subparser.add_argument('--log-file', help="Filename where the logs from the scheduler are written. This file is"
                                                  " appended to every invocation", default="/var/log/airbox.log")

    def run(self):
        out_fname = '/etc/cron.hourly/airbox'
        script = CRON_SCIPT.format(
            python=abspath(sys.executable),
            cli_script=abspath(sys.argv[0]),
            config_fname=abspath(config['config']),
            log_file=abspath(config['log_file'])
        )
        logger.info('writing to {}:\n{}'.format(out_fname, script))

        try:
            with open(out_fname, 'w') as fh:
                fh.write(script)

            logger.info('Setting {} to be executable (755)'.format(out_fname))
            chmod(out_fname, 0o755)
            logger.info('Cron script successfully installed')
        except PermissionError:
            logger.exception("Cannot install cron script. Rerun command as sudo")