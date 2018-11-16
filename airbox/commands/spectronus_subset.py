from datetime import datetime, timedelta
from logging import getLogger
from os.path import join

from airbox import config
from airbox.dir import get_plot_dir
from airbox.mail import sendmail
from airbox.plotters.spectronus import SpectronusPlotter
from .base import BaseCommand

logger = getLogger(__name__)

MESSAGE_TEMPLATE = """Find attached the spectronus data resampled to mean values over 10min periods.

Contact Jared (jared.lewis@unimelb.edu.au or jared.lewis@aurora.aad.gov.au) for any suggested changes.
"""


class SpectronusSubsetCommand(BaseCommand):
    """
    Takes the last 24 hours of spectronus data, decimates it and then emails the result to Dave Griffiths.
    """
    name = 'spectronus_subset'
    help = 'Extract a subset of spectronus data'

    def initialise_parser(self, subparser):
        yesterday = datetime.utcnow() - timedelta(days=1)
        subparser.add_argument('-d', '--date', help='Date to generate plots for. Should be formatted as YYYY-MM-DD. '
                                                    'Defaults to yesterday if no value is provided.',
                               default=yesterday.date().isoformat())

    def run(self):
        try:
            date = config['date']
            d = datetime.strptime(date, '%Y-%m-%d')
            d = d.date()
        except KeyError:
            yesterday = datetime.utcnow() - timedelta(days=1)
            d = yesterday.date()

        p = SpectronusPlotter()
        df = p.get_day(d)
        d_str = d.isoformat()

        logger.info('Loaded data for day: {}'.format(config['date']))

        csv_fname = join(get_plot_dir(), 'airbox_spectronus_10min_{}.csv'.format(d_str))
        resampled_df = df.resample('5T').mean()
        resampled_df.to_csv(csv_fname, float_format="%.4f")
        logger.info('Dumped data to {}'.format(csv_fname))

        message = MESSAGE_TEMPLATE.format(d_str)
        sendmail(
            config['email_to'] + config['email_expeditioners'],
            'Spectronus summary for {}'.format(d_str),
            message,
            attachments=[('application/csv', csv_fname)]
        )
