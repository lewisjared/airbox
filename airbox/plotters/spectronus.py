from glob import glob
from os.path import join

import pandas as pd

from airbox.dir import get_instr_dir
from .base import BasePlotter


class SpectronusPlotter(BasePlotter):
    name = 'spectronus'

    def get_day(self, d):
        """
        Get a day of spectronus data
        :param d: Date to extract
        :return: Pandas dataframe
        """
        fnames = glob(join(get_instr_dir('Spectronus/Output'), '{}{:02}{:02}_*'.format(str(d.year)[2:], d.month, d.day)))
        if len(fnames) == 0:
            raise FileNotFoundError("Couldn't find any spectronus data")

        df = pd.DataFrame()
        for f in fnames:
            data = pd.read_csv(f, parse_dates=[0], index_col=0)
            df = pd.merge(df, data, how='outer', left_index=True, right_index=True)
        return df[df.index.date == d]
