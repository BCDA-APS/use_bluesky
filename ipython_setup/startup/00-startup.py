print(__file__)

"""connect with Bluesky"""

from bluesky import RunEngine
from bluesky.utils import get_history
RE = RunEngine(get_history())

# Import matplotlib and put it in interactive mode.
import matplotlib.pyplot as plt
plt.ion()

# Make plots update live while scans run.
from bluesky.utils import install_qt_kicker
install_qt_kicker()

# Optional: set any metadata that rarely changes. in 60-metadata.py

# convenience imports
from bluesky.callbacks import *
from bluesky.plan_tools import print_summary
import bluesky.plans as bp
import bluesky.plan_stubs as bps
import bluesky.plan_patterns as bpp
from time import sleep
import numpy as np
import bluesky.magics


# Uncomment the following lines to turn on 
# verbose messages for debugging.
import logging
# ophyd.logger.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)


# diagnostics
from bluesky.utils import ts_msg_hook
#RE.msg_hook = ts_msg_hook
from bluesky.simulators import summarize_plan
