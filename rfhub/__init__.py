import pkg_resources
__version__ = pkg_resources.require("robotframework-hub")[0].version

import kwdb

# this will be defined once the app starts
KWDB = None 
