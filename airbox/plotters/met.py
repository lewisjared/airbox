from os.path import join

import pandas as pd

from .base import BasePlotter

'datetime'


class MetPlotter(BasePlotter):
    name = 'met'

    columns = [
        'datetime',
        'temperature',
        'dewpoint',
        'relHumidity',
        'windHeaterTemp.',
        'R2SHeaterTemp.',
        'wetBulbTemperature',
        'absHumidity',
        'mixingRatio',
        'specificEnthalpy',
        'pressure',
        'windSpeed',
        'airDensity',
        'windSpeedVct',
        'windDir',
        'windDirVct',
        'precipitationAbs',
        'precipitationType',
        'globalRadiation'
    ]

    units = [
        None,
        u'°C',
        u'°C',
        u'%',
        u'°C',
        u'°C',
        u'°C',
        u'g/m³',
        u'g/kg',
        u'kJ/kg',
        u'hPa',
        u'm/s',
        u'kg/m³',
        u'm/s',
        u'°',
        u'°',
        u'mm',
        u'logic',
        u'W/m²',
    ]

    def get_day(self, d):
        """
        Get a day of met data
        :param d: Date to extract
        :return: Pandas dataframe
        """
        fname = '{}-{:02}-{:02}Values.Txt'.format(d.year, d.month, d.day)
        data = pd.read_csv(join('/mnt/aurora/Data/v1/raw/WeatherStation', fname), parse_dates=[0], index_col=0,
                           names=self.columns, header=None, skiprows=5, sep=';')

        return data[data.index.date == d]
