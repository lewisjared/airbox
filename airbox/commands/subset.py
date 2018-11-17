from datetime import datetime, timedelta
from logging import getLogger
from os.path import join

from airbox import config
from airbox.dir import get_plot_dir
from airbox.plotters import _plotters
from .base import BaseCommand

logger = getLogger(__name__)

MESSAGE_TEMPLATE = """Find attached the data from {instrument} resampled to mean values over {period}min periods.

Contact Jared (jared.lewis@unimelb.edu.au or jared.lewis@aurora.aad.gov.au) for any suggested changes.
"""


class SubsetCommand(BaseCommand):
    """
    Takes the last 24 hours of data, decimates it and then emails the result.
    """
    name = 'subset'
    help = 'Extract (and optionally send), a csv file containing the data for a given instrument for a given day. The' \
           ' data is resampled to reduce the size of the file'

    def initialise_parser(self, subparser):
        yesterday = datetime.utcnow() - timedelta(days=1)
        subparser.add_argument('-d', '--date', help='Date to generate plots for. Should be formatted as YYYY-MM-DD. '
                                                    'Defaults to yesterday if no value is provided.',
                               default=yesterday.date().isoformat())

        subparser.add_argument('--period',
                               help='The number of minutes between measurements',
                               default=10)

        subparser.add_argument('--instrument',
                               help='The instrument to dump. Options include: {}'.format([p.name for p in _plotters]),
                               required=True)

    def run(self):
        try:
            date = config['date']
            d = datetime.strptime(date, '%Y-%m-%d')
            d = d.date()
        except KeyError:
            yesterday = datetime.utcnow() - timedelta(days=1)
            d = yesterday.date()

        for Plter in _plotters:
            if Plter.name != config['instrument']:
                continue

            p = Plter()
            df = p.get_day(d)

            d_str = d.isoformat()

            logger.info('Loaded data for day: {}'.format(config['date']))

            csv_fname = join(get_plot_dir(),
                             'airbox_{}_{}min_{}.csv'.format(config['instrument'], config['period'], d_str))
            resampled_df = df.resample('{}T'.format(config['period'])).mean()
            resampled_df.to_csv(csv_fname, float_format="%.4f")
            logger.info('Dumped data to {}'.format(csv_fname))
