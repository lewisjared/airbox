class BaseCommand(object):
    name = ''
    help = ''

    def initialise_parser(self, subparser):
        """
        Set up commandline arguments

        Any arguments specified will be added to `airbox.config` using the dest as a key.
        :see: argparse
        :param subparser: An argparse subparser
        """
        pass

    def run(self):
        """
        Run the command.

        This function should be overridden to perform the functionality required by the command.
        :return:
        """
        pass
