class BaseCommand(object):
    name = ''
    help = ''

    def initialise_parser(self, subparser):
        pass

    def run(self, config, args):
        pass