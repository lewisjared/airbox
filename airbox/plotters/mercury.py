from io import StringIO
from os.path import exists, join

import pandas as pd

from airbox.dir import get_instr_dir
from .base import BasePlotter


class MercuryPlotter(BasePlotter):
    name = 'tekran'
    columns = [
        "datetime",
        "type",
        "c",
        "stat",
        "zero",
        "adTim",
        "vol",
        "bl",
        "blDev",
        "maxV",
        "area",
        "hg"
    ]

    def get_day(self, d):
        """
        Get a day of mercury data
        :param d: Date to extract
        :return: Pandas dataframe
        """
        fname = join(get_instr_dir('Tekran'), 'AA{}{:02}{:02}.txt'.format(str(d.year)[2:], d.month, d.day))
        if not exists(fname):
            raise FileNotFoundError(fname)

        lines = open(fname).readlines()
        valid_lines = []
        for l in lines:
            toks = l.split()
            if len(toks) == len(self.columns) + 1:  # The date and time cols are split
                # add a leading 20 to change dates to 2018 instead of 18
                valid_lines.append("20" + toks[0] + " " + ",".join(toks[1:]))

        # Recreate a stream only containing valid lines for parsing by pandas
        buff = StringIO("\n".join(valid_lines))
        data = pd.read_csv(buff, parse_dates=[0], index_col=0, header=None, names=self.columns)

        data = data[data['type'] == 'CONT']
        return data[data.index.date == d]
