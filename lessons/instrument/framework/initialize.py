
"""
initialize the bluesky framework
"""

__all__ = [
    'RE', 'db', 'sd',
    'bec', 'peaks',
    'bp', 'bps', 'bpp',
    'summarize_plan',
    'np',
    'callback_db',
    ]

from ..session_logs import logger
logger.info(__file__)

from bluesky import RunEngine
from bluesky import SupplementalData
from bluesky.callbacks.best_effort import BestEffortCallback
from bluesky.callbacks.broker import verify_files_saved
from bluesky.magics import BlueskyMagics
from bluesky.utils import PersistentDict
from bluesky.utils import ProgressBarManager
from bluesky.utils import ts_msg_hook
from IPython import get_ipython
import databroker
import ophyd
import warnings

# convenience imports
# from bluesky.callbacks import *
# from bluesky.callbacks.broker import *
# from bluesky.simulators import *
from bluesky.simulators import summarize_plan
import bluesky.plan_stubs as bps
import bluesky.plans as bp
import bluesky.preprocessors as bpp
import numpy as np


# Set up a RunEngine and use metadata backed PersistentDict
RE = RunEngine({})
RE.md = {}      # empty dict for lessons
# RE.md = PersistentDict(   # beam line use
#     os.path.join(os.environ["HOME"], ".config", "Bluesky_RunEngine_md")
# )

# keep track of callback subscriptions
callback_db = {}

# Set up a Broker.
db = databroker.temp().v1

# Subscribe metadatastore to documents.
# If this is removed, data is not saved to metadatastore.
callback_db['db'] = RE.subscribe(db.insert)

# Set up SupplementalData.
sd = SupplementalData()
RE.preprocessors.append(sd)

# Add a progress bar.
pbar_manager = ProgressBarManager()
RE.waiting_hook = pbar_manager

# Register bluesky IPython magics.
get_ipython().register_magics(BlueskyMagics)

# Set up the BestEffortCallback.
bec = BestEffortCallback()
callback_db['bec'] = RE.subscribe(bec)
peaks = bec.peaks  # just an alias, for less typing
bec.disable_baseline()

# At the end of every run, verify that files were saved and
# print a confirmation message.
# callback_db['post_run_verify'] = RE.subscribe(post_run(verify_files_saved), 'stop')


# Uncomment the following lines to turn on
# verbose messages for debugging.
# ophyd.logger.setLevel(logging.DEBUG)

# diagnostics
#RE.msg_hook = ts_msg_hook

# set default timeout for all EpicsSignal connections & communications
if hasattr(ophyd, ""):
    ophyd.EpicsSignalBase.set_defaults(
        auto_monitor=True,
        timeout=60,
        write_timeout=60,
        connection_timeout=5,
    )
else:
    warnings.warn(
        f"Version of ophyd {ophyd.__version__} is old,"
        " upgrade to 1.6.0+ to get set_defaults() method."
        "  Cannot set default: auto_monitor=True to use CA cache."
    )
    ophyd.EpicsSignalBase.set_default_timeout(
        timeout=10, 
        connection_timeout=5
    )
