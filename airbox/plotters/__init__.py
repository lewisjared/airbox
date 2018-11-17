import pandas as pd

from .cpc import CN3Plotter, CN10Plotter
from .mercury import MercuryPlotter
from .met import MetPlotter
from .ozone import OzonePlotter
from .radon import RadonPlotter
from .spectronus import SpectronusPlotter

_plotters = [
    #CN3Plotter,
    #CN10Plotter,
    MercuryPlotter,
    MetPlotter,
    OzonePlotter,
    RadonPlotter,
    SpectronusPlotter
]


def get_data_for_day(d):
    """
    Gets all (plottable) airbox data for a given day.

    The results is a pandas dataframe containing all data which can be loaded. Note that due to differences between the
    sampling periods of the instruments, not all time periods may contain data.

    A day is a 0000-2359 UTC
    :param d: Date
    :return: pandas Dataframe. The column names for each instrument will be prefixed with the instrument name to avoid
        conflicts. For example 'radon_ExFlow' is the 'ExFlow' variable from the radon instrument
    """

    df = pd.DataFrame()

    for Plotter in _plotters:
        p = Plotter()
        data = p.get_day(d)
        data.columns = ['{}_{}'.format(p.name, c.strip()) for c in data.columns]
        # Merge the dataframes together
        df = pd.merge(df, data, how='outer', left_index=True, right_index=True)
    df = df.sort_index()
    return df
