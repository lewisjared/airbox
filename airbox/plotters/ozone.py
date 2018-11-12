import pandas as pd

from .base import BasePlotter


class OzonePlotter(BasePlotter):
    name = 'ozone'

    def get_day(self, d):
        """
        Get a day of ozone data
        :param d: Date to extract
        :return: Pandas dataframe
        """
        data = pd.read_csv('/mnt/aurora/Data/v1/raw/Ozone/49i 101718 0443 AA.dat', delim_whitespace=True, skiprows=5,
                           parse_dates=[[0, 1]], index_col=0)

        return data[data.index.date == d]
