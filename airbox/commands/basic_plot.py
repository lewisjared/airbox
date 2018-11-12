from datetime import datetime
from logging import getLogger
import matplotlib.pyplot as plt
from airbox.plotters import get_data_for_day
from .base import BaseCommand

logger = getLogger(__name__)


class BasicPlotCommand(BaseCommand):
    """
    Takes the last 24 hours of spectronus data, decimates it and then emails the result to Dave Griffiths.
    """
    name = 'basic_plot'
    help = 'Create a generic plot'

    def initialise_parser(self, subparser):
        subparser.add_argument('-d', '--date', help='Date to generate plots for. Should be formatted as YYYY-MM-DD.',
                               required=True)

    def plot_variable(self, df, var, units, **kwargs):
        vals = df[var].dropna()
        ax = vals.plot(label=var, legend=True, **kwargs)
        ax.set_ylabel(units)

    def run(self, config, args):
        d = datetime.strptime(args.date, '%Y-%m-%d')
        d = d.date()

        df = get_data_for_day(d)
        logger.info('Loaded data for day: {}'.format(args.date))

        self.plot_variable(df, 'radon_ExFlow', 'm3/hour', secondary_y=True)
        self.plot_variable(df, 'ozone_o3', 'ppb')

       # plt.legend()
        plt.show()