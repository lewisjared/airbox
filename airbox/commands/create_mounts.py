from os.path import join

from airbox import config
from .backup import ROOT_MOUNT_POINT
from .base import BaseCommand


class CreateMountsCommand(BaseCommand):
    name = 'create_mounts'
    help = 'Print the command needed to create all of the directories needed to mount the data.\n' \
           'This command needs to be run as sudo using "sudo `airbox create_mounts`'

    def run(self):
        lines = []
        for instr in config['instruments']:
            source = join(ROOT_MOUNT_POINT, instr['node']['name'], instr['mount_name'])

            lines.append(source)

        # Dump the output
        print('mkdir -p ' + ' '.join(set(lines)))
