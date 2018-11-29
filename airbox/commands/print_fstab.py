from os.path import join

from airbox import config
from .backup import ROOT_MOUNT_POINT
from .base import BaseCommand


class PrintFstabCommand(BaseCommand):
    name = 'print_fstab'
    help = 'Dump the configuration needed in /etc/fstab for mounting all of the instruments'

    def run(self):
        lines = []
        for instr in config['instruments']:
            node = instr['node']

            # Ensure that the directory is mounted
            source = join(ROOT_MOUNT_POINT, instr['node']['name'], instr['mount_name'])

            kwargs = {
                'user': node['user'],
                'pass': node['pass'],
                'uid': 1000,
                'gid': 1000,
                'iocharset': 'utf8'
            }
            opts = ','.join(['{}={}'.format(k, kwargs[k]) for k in kwargs]) + ',noperm,nofail'
            mount_path = '//{}/{}'.format(node['ip'], instr['mount_name'])
            lines.append('\t'.join([mount_path, source, "cifs", opts, "0", "0"]))

        # Dump the output
        print('\n'.join(set(lines)))
