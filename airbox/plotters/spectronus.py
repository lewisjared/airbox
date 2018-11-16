from glob import glob
from os.path import join
from datetime import timedelta

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
        d_dir = get_instr_dir('Spectronus/Output')
        fnames = glob(join(d_dir, '{}{:02}{:02}_*'.format(str(d.year)[2:], d.month, d.day)))
        # include the first file for the next day
        next_day = d + timedelta(days=1)
        fnames.extend(glob(join(d_dir, '{}{:02}{:02}_04*'.format(str(next_day.year)[2:], next_day.month, next_day.day))))
        if len(fnames) == 0:
            raise FileNotFoundError("Couldn't find any spectronus data")

        df = None
        for f in fnames:
            data = pd.read_csv(f, parse_dates=[0], index_col=0, sep=', ')
            if df is None:
                df = data
            else:
                df = df.append(data)
        return df[df.index.date == d]
