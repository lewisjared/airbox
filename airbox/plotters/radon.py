from calendar import month_abbr
from os.path import join

import pandas as pd

from airbox.dir import get_instr_dir
from .base import BasePlotter


class RadonPlotter(BasePlotter):
    name = 'radon'

    def get_day(self, d):
        """
        Get a day of radon data
        :param d: Date to extract
        :return: Pandas dataframe
        """
        fname = 'AI{}{}.CSV'.format(month_abbr[d.month].capitalize(), str(d.year)[2:])
        data = pd.read_csv(join(get_instr_dir('Radon'), fname), parse_dates=[[0, 2, 3, 4]], index_col=0)
        # Col incorrectly named in output
        data.columns.values[5] = 'Radon'
        return data[data.index.date == d]
