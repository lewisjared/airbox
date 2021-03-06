import matplotlib

# Only use core pdf fonts to save size
matplotlib.rcParams['pdf.use14corefonts'] = True
matplotlib.rcParams['legend.fontsize'] = 5

__version__ = '1.0.2'

from .configstore import ConfigStore

config = ConfigStore()
