"""
Utilities for calling linux processes

Uses subprocess.run to execute the subcommands
"""

from subprocess import run, PIPE, CalledProcessError, list2cmdline
from logging import getLogger


logger = getLogger(__name__)

FAILED_CMD_MSG = """Command returned a non-zero code.
STDOUT:
{}
==========================
STDERR:
{}
========================
"""


def run_command(args, can_ret_nonzero=False):
    logger.debug('Running command: {}'.format(list2cmdline(args)))
    try:
        res = run(args, check=not can_ret_nonzero, stdout=PIPE, stderr=PIPE)
        logger.debug('STDOUT:\n' + res.stdout.decode())
        logger.debug('STDERR:\n' + res.stderr.decode())
        return res
    except CalledProcessError as e:
        logger.error(FAILED_CMD_MSG.format(e.stdout.decode(), e.stderr.decode()))
        raise
