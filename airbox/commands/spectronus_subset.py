from logging import getLogger

from .base import BaseCommand

logger = getLogger(__name__)


class SpectronusSubsetCommand(BaseCommand):
    """
    Takes the last 24 hours of spectronus data, decimates it and then emails the result to Dave Griffiths.
    """
    name = 'spectronus_subset'
    help = 'Extract a subset of spectronus data'

    def run(self, config, args):
        logger.info('Testing')

    def initialise_parser(self, subparser):
        pass
