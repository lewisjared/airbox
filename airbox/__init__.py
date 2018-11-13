import matplotlib

# Only use core pdf fonts to save size
matplotlib.rcParams['pdf.use14corefonts'] = True
matplotlib.rcParams['legend.fontsize'] = 'small'

from .configstore import ConfigStore

config = ConfigStore()
