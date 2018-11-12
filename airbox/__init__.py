import matplotlib

# Only use core pdf fonts to save size
matplotlib.rcParams['pdf.use14corefonts'] = True

from .configstore import ConfigStore

config = ConfigStore()
