import pkg_resources
from .version import __version__

from . import kwdb

# this will be defined once the app starts
KWDB = None
