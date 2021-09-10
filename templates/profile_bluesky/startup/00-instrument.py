
"""
start bluesky in IPython session for INSTRUMENT
"""

import os
import pathlib
import sys

# uncomment when "~/bluesky/instrument" directory exists
# Allows startup from any directory
# path = os.path.join(pathlib.Path.home(), "bluesky")
# sys.path.append(path)

from instrument.collection import *

# show_ophyd_symbols()
# print_RE_md(printing=False)
