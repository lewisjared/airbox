from glob import glob
from logging import getLogger
from os.path import join

import numpy as np
import pandas as pd

from airbox.dir import get_instr_dir
from .base import BasePlotter

logger = getLogger(__name__)


def skip_rows(l):
    if l == 3: return False
    return not (l % 5 == 4)

def read_cpc_csv(read_filename):
    """
    Reads CPC data exports from AIM 10 and higher as row based, with
    ONLY concentration data output

    Adapted from Ruhi Humpries code for reading CPCs
    """

    # Read each row of data, taking into account that each row can change length and parsing format (weird...)
    df = pd.read_csv(read_filename, skiprows=skip_rows, engine='python', skipinitialspace=True, iterator=True,
                     chunksize=1000, sep=',')


    out = None

    for chunk in df:
        # Extract initial timestamp for each sample (i.e. each row)
        try:
            chunk['sample_timestamp'] = pd.to_datetime(chunk['Start Date'] + ' ' + chunk['Start Time'],
                                                       format='%m/%d/%y %H:%M:%S')
            chunk = chunk.reset_index()
            del chunk['index']
        except KeyError:
            # The csv file that you've read isn't actually a TSI CPC file
            return

        data = pd.DataFrame(columns={'Timestamp', 'Concentration', 'Counts', 'Analog 1', 'Analog 2'})
        for rowidx in range(0, len(chunk)):

            # Create timestamp and extract concentration, counts, and analog inputs (where available) for each sample in chunk
            timestamp = [chunk['sample_timestamp'][rowidx] + pd.Timedelta(seconds=x) for x in
                         range(0, chunk['Sample Length'][rowidx])]

            #           conc = chunk.loc[rowidx][12:(12+chunk['Sample Length'][rowidx])]

            cols_conc = [c for c in chunk.columns if 'Conc (#' in c]
            if len(cols_conc) > 0:
                conc = chunk.loc[rowidx][cols_conc][0:chunk['Sample Length'][rowidx]]
            else:
                conc = pd.Series(np.nan, index=np.arange(0, len(timestamp)))

            cols_count = [c for c in chunk.columns if 'Count' in c]
            if len(cols_count) > 0:
                count = chunk.loc[rowidx][cols_count][0:chunk['Sample Length'][rowidx]]
            else:
                count = pd.Series(np.nan, index=np.arange(0, len(timestamp)))

            cols_analog1 = [c for c in chunk.columns if 'Analog 1' in c]
            if len(cols_analog1) > 0:
                a1 = chunk.loc[rowidx][cols_analog1][0:chunk['Sample Length'][rowidx]]
            else:
                a1 = pd.Series(np.nan, index=np.arange(0, len(timestamp)))

            cols_analog2 = [c for c in chunk.columns if 'Analog 2' in c]
            if len(cols_analog2) > 0:
                a2 = chunk.loc[rowidx][cols_analog2][0:chunk['Sample Length'][rowidx]]
            else:
                a2 = pd.Series(np.nan, index=np.arange(0, len(timestamp)))

            logger.debug('Formatting sample ' + str(chunk['Sample #'].loc[rowidx])
                         + 'from file ' + read_filename)

            # Format data as dataframe
            data_temp = pd.DataFrame({'Timestamp': timestamp,
                                      'Concentration': conc.values,
                                      'Counts': count.values,
                                      'Analog 1': a1.values,
                                      'Analog 2': a2.values})

            # Append new data to current data
            data = pd.concat([data, data_temp])

        # Drop empty columns
        for col in data.columns:
            if data[col].count() == 0:
                del data[col]

        if len(data) != 0:
            # Drop duplicates that may be present
            data = data.drop_duplicates(subset='Timestamp', keep='last')
            # Set index
            data = data.set_index('Timestamp')
            # Coerce data to the correct type, dealing with infinite values output from AIM
            for col in data.columns:
                data[col] = [np.nan if x == '1.#INF' else float(x) for x in data[col]]

            if out is not None:
                out = out.append(data)
            else:
                out = data
    return out


class CPCPlotter(BasePlotter):
    name = 'cpc'
    instrument_name = None

    def get_day(self, d):
        """
        Get a day of mercury data
        :param d: Date to extract
        :return: Pandas dataframe
        """
        fnames = glob(join(get_instr_dir(self.instrument_name), '*.csv'))
        assert len(fnames)

        fname = fnames[-1]  # Assuming that the files are named correctly then the most recent file will be last
        data = read_cpc_csv(fname)
        return data[data.index.date == d]


class CN3Plotter(CPCPlotter):
    name = 'cn3'
    instrument_name = 'CPC3772'


class CN10Plotter(CPCPlotter):
    name = 'cn10'
    instrument_name = 'CPC3776'
