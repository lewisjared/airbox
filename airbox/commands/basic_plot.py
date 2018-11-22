from datetime import datetime, timedelta
from logging import getLogger
from os.path import join

import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator

from airbox import config
from airbox.dir import get_plot_dir
from airbox.mail import sendmail
from airbox.plotters import get_data_for_day
from .base import BaseCommand

logger = getLogger(__name__)

MESSAGE_TEMPLATE = """Find attached a summary of the measurements made by Airbox during {}.

Contact Jared (jared.lewis@unimelb.edu.au or jared.lewis@aurora.aad.gov.au) for any suggested changes.
"""


class BasicPlotCommand(BaseCommand):
    """
    Takes the last 24 hours of spectronus data, decimates it and then emails the result to Dave Griffiths.
    """
    name = 'basic_plot'
    help = 'Create a generic plot'

    def initialise_parser(self, subparser):
        yesterday = datetime.utcnow() - timedelta(days=1)
        subparser.add_argument('-d', '--date', help='Date to generate plots for. Should be formatted as YYYY-MM-DD. '
                                                    'Defaults to yesterday if no value is provided.',
                               default=yesterday.date().isoformat())
        subparser.add_argument('--send-email',
                               help='If specified, than an email containing the plot will be sent to the list of '
                                    'recipients specified in `email_to`',
                               action='store_true', default=False)
        subparser.add_argument('--dump-timeseries',
                               help='If specified, a CSV containing the data used to generate the plots and some '
                                    'additional variables will be dumped to file in the `plots` directory',
                               action='store_true', default=False)

    def plot_variable(self, df, var, units, **kwargs):
        try:
            vals = df[var].dropna()
            vals.index = vals.index.time
            ax = vals.plot(label=var, legend=True, **kwargs)
            ax.set_ylabel(units)
        except TypeError:
            logger.warning("No data to plot for {}".format(var))

    def run(self):
        try:
            date = config['date']
            d = datetime.strptime(date, '%Y-%m-%d')
            d = d.date()
        except KeyError:
            yesterday = datetime.utcnow() - timedelta(days=1)
            d = yesterday.date()

        df = get_data_for_day(d)
        logger.info('Loaded data for day: {}'.format(d.isoformat()))
        fig, axs = plt.subplots(6, 1, sharex=True, figsize=(6.4, 8.4))

        self.plot_variable(df, 'met_pressure', 'hPa', ax=axs[0], secondary_y=True)
        self.plot_variable(df, 'met_temperature', 'degC', ax=axs[0])

        self.plot_variable(df, 'radon_TankP', '', ax=axs[1], secondary_y=True)
        self.plot_variable(df, 'radon_ExFlow', '', ax=axs[1])
        self.plot_variable(df, 'radon_Radon', '', ax=axs[1])

        self.plot_variable(df, 'ozone_o3', 'ppb', ax=axs[2], secondary_y=True)
        self.plot_variable(df, 'tekran_hg', 'ng/m3', ax=axs[2])

        self.plot_variable(df, 'ozone_flowa', '', ax=axs[3], secondary_y=True)
        self.plot_variable(df, 'ozone_pres', '', ax=axs[3])

        self.plot_variable(df, 'spectronus_Room_Temperature_Avg', 'degC', ax=axs[4], secondary_y=True)
        self.plot_variable(df, 'spectronus_Cell_Temperature_Avg', 'degC', ax=axs[4], secondary_y=True)
        self.plot_variable(df, 'spectronus_Flow_In_Avg', '', ax=axs[4])
        self.plot_variable(df, 'spectronus_Flow_Out_Avg', '', ax=axs[4])

        self.plot_variable(df, 'spectronus_CO2', '', ax=axs[5])
        self.plot_variable(df, 'spectronus_CO', '', ax=axs[5])
        self.plot_variable(df, 'spectronus_H2O', '', ax=axs[5], secondary_y=True)


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

        fname = join(get_plot_dir(), 'airbox_summary_{}.pdf'.format(d_str))
        plt.savefig(fname)
        logger.info('Figure saved to {}'.format(fname))
        created_files = [('application/pdf', fname)]

        if config['dump_timeseries']:
            csv_fname = join(get_plot_dir(), 'airbox_summary_timeseries_{}.csv'.format(d_str))
            resampled_df = df.resample('10T').mean()
            resampled_df.to_csv(csv_fname, float_format="%.4f")
            logger.info('Dumped data to {}'.format(csv_fname))
            created_files.append(('application/csv', csv_fname))

        if config['send_email']:
            message = MESSAGE_TEMPLATE.format(d_str)
            sendmail(
                config['email_to'] + config['email_expeditioners'],
                'Airbox summary for {}'.format(d_str),
                message,
                attachments=created_files
            )
