print(__file__)
# Make ophyd listen to pyepics.
from ophyd import setup_ophyd
setup_ophyd()

# Define some environment variables (for now)
import os

# Import matplotlib and put it in interactive mode.
import matplotlib.pyplot as plt
plt.ion()

# Make plots update live while scans run.
from bluesky.utils import install_qt_kicker
install_qt_kicker()

# Optional: set any metadata that rarely changes. in 60-metadata.py

# convenience imports
#from ophyd.commands import *		# old-style
from bluesky.callbacks import *
#from bluesky.spec_api import *		# old-style
#from bluesky.global_state import gs, abort, stop, resume   # old-style
from bluesky.plan_tools import print_summary
import bluesky.plans as bp
from time import sleep
import numpy as np

