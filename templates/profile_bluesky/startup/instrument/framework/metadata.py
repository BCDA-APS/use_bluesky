
"""
"""

__all__ = []

from ..session_logs import logger
logger.info(__file__)

import apstools
import bluesky
import databroker
from datetime import datetime
import epics
import getpass
import h5py
import matplotlib
import numpy
import ophyd
import os
import pyRestTable
import socket
import spec2nexus

from .initialize import RE

# Set up default metadata

RE.md['beamline_id'] = 'APS INSTRUMENT'
RE.md['proposal_id'] = 'testing'
RE.md['pid'] = os.getpid()

HOSTNAME = socket.gethostname() or 'localhost' 
USERNAME = getpass.getuser() or 'APS INSTRUMENT user' 
RE.md['login_id'] = USERNAME + '@' + HOSTNAME

# useful diagnostic to record with all data
RE.md['versions'] = {}
RE.md['versions']['apstools'] = apstools.__version__
RE.md['versions']['bluesky'] = bluesky.__version__
RE.md['versions']['databroker'] = databroker.__version__
RE.md['versions']['epics'] = epics.__version__
RE.md['versions']['matplotlib'] = matplotlib.__version__
RE.md['versions']['numpy'] = numpy.__version__
RE.md['versions']['ophyd'] = ophyd.__version__
RE.md['versions']['pyRestTable'] = pyRestTable.__version__
RE.md['versions']['spec2nexus'] = spec2nexus.__version__
