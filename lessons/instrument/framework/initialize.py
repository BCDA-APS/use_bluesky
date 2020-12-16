
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
# from bluesky.utils import PersistentDict

# Set up a RunEngine and use metadata backed PersistentDict
RE = RunEngine({})
RE.md = {}      # empty dict for lessons
# RE.md = PersistentDict(   # beam line use
#     os.path.join(os.environ["HOME"], ".config", "Bluesky_RunEngine_md")
# )

# keep track of callback subscriptions
callback_db = {}

# Set up a Broker.
import databroker
db = databroker.temp().v1

# Subscribe metadatastore to documents.
# If this is removed, data is not saved to metadatastore.
callback_db['db'] = RE.subscribe(db.insert)

# Set up SupplementalData.
from bluesky import SupplementalData
sd = SupplementalData()
RE.preprocessors.append(sd)

# Add a progress bar.
from bluesky.utils import ProgressBarManager
pbar_manager = ProgressBarManager()
RE.waiting_hook = pbar_manager

# Register bluesky IPython magics.
from IPython import get_ipython
from bluesky.magics import BlueskyMagics
get_ipython().register_magics(BlueskyMagics)

# Set up the BestEffortCallback.
from bluesky.callbacks.best_effort import BestEffortCallback
bec = BestEffortCallback()
callback_db['bec'] = RE.subscribe(bec)
peaks = bec.peaks  # just an alias, for less typing
bec.disable_baseline()

# At the end of every run, verify that files were saved and
# print a confirmation message.
from bluesky.callbacks.broker import verify_files_saved
# callback_db['post_run_verify'] = RE.subscribe(post_run(verify_files_saved), 'stop')

# convenience imports
# from bluesky.callbacks import *
# from bluesky.callbacks.broker import *
# from bluesky.simulators import *
import bluesky.plans as bp
import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp
import numpy as np

# Uncomment the following lines to turn on 
# verbose messages for debugging.
# ophyd.logger.setLevel(logging.DEBUG)

# diagnostics
from bluesky.utils import ts_msg_hook
#RE.msg_hook = ts_msg_hook
from bluesky.simulators import summarize_plan

# set default timeout for all EpicsSignal connections & communications
import ophyd
ophyd.EpicsSignalBase.set_default_timeout(timeout=10, connection_timeout=5)
