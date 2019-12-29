from rfhub import app
import sys
from .version import __version__

if sys.version_info < (3,6):
    print("rfhub {} requires python 3.6 or above".format(__version__))
    sys.exit(1)

app.hub = app.RobotHub()
app.hub.start()
