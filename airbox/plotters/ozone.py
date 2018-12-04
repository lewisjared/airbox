import pandas as pd

from airbox.dir import get_instr_dir
from .base import BasePlotter
from airbox import  config


class OzonePlotter(BasePlotter):
    name = 'ozone'

    def get_day(self, d):
        """
        Get a day of ozone data
        :param d: Date to extract
        :return: Pandas dataframe
        """
        inst = config.get_instrument('Ozone')
        data = pd.read_csv(get_instr_dir('Ozone/{}'.format(inst['filter'])), delim_whitespace=True, skiprows=5,
                           parse_dates=[[0, 1]], index_col=0)

        return data[data.index.date == d]
