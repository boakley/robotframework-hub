import pkg_resources
from .version import __version__

from rfhub import kwdb

# this will be defined once the app starts
KWDB = None
