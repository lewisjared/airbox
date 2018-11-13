from datetime import datetime
from logging import getLogger

import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator

from airbox import config
from airbox.mail import sendmail
from airbox.plotters import get_data_for_day
from .base import BaseCommand

logger = getLogger(__name__)

MESSAGE_TEMPLATE = """Find attached a summary of the measurements made by Airbox during {}.
"""


class BasicPlotCommand(BaseCommand):
    """
    Takes the last 24 hours of spectronus data, decimates it and then emails the result to Dave Griffiths.
    """
    name = 'basic_plot'
    help = 'Create a generic plot'

    def initialise_parser(self, subparser):
        subparser.add_argument('-d', '--date', help='Date to generate plots for. Should be formatted as YYYY-MM-DD.',
                               required=True)
        subparser.add_argument('--send-email',
                               help='If specified, than an email containing the plot will be sent to the list of '
                                    'recipients specified in `email_to`',
                               action='store_true', default=False)

    def plot_variable(self, df, var, units, **kwargs):
        vals = df[var].dropna()
        vals.index = vals.index.time
        ax = vals.plot(label=var, legend=True, **kwargs)
        ax.set_ylabel(units)

    def run(self):
        d = datetime.strptime(config['date'], '%Y-%m-%d')
        d = d.date()

        df = get_data_for_day(d)
        logger.info('Loaded data for day: {}'.format(config['date']))
        fig, axs = plt.subplots(3, 1, sharex=True)

        self.plot_variable(df, 'met_pressure', 'hPa', ax=axs[0], secondary_y=True)
        self.plot_variable(df, 'met_temperature', 'degC', ax=axs[0])

        self.plot_variable(df, 'radon_TankP', '', ax=axs[1], secondary_y=True)
        self.plot_variable(df, 'radon_ExFlow', '', ax=axs[1])
        self.plot_variable(df, 'radon_Radon', '', ax=axs[1])

        self.plot_variable(df, 'ozone_o3', 'ppb', ax=axs[2], secondary_y=True)
        self.plot_variable(df, 'tekran_hg', 'ng/m3', ax=axs[2])


        # set up the limits of the plot. Note that the locations are defined in seconds
        plt.xlim(0, 24 * 60 * 60)
        axs[0].get_xaxis().set_major_locator(FixedLocator([x * 60 * 60 for x in range(0, 24 + 1, 6)]))
        axs[0].get_xaxis().set_minor_locator(FixedLocator([x * 60 * 60 for x in range(0, 24 + 1)]))

        # Turn on grid every 6 hours
        for a in axs:
            a.get_xaxis().grid(True, 'major')

        plt.tight_layout(rect=(0, 0, 1, 0.95))
        d_str = d.isoformat()
        plt.suptitle('Summary timeseries from Airbox for {} (UTC)'.format(d_str))

        plt.savefig('airbox_summary_{}.pdf'.format(d_str))

        if config['send_email']:
            message = MESSAGE_TEMPLATE.format(d_str)
            sendmail(
                config['email_to'],
                'Airbox summary for {}'.format(d_str),
                message,
                attachments=['airbox_summary_{}.pdf'.format(d_str)]
            )
