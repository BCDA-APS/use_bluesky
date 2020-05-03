
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

# add parent directory of instrument package to import path
import os, sys
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
        )
    )
)

from bluesky import RunEngine
from bluesky.utils import PersistentDict

def get_md_path():
    md_dir_name = "Bluesky_RunEngine_md"
    if os.environ == "win32":
        home = os.environ["LOCALAPPDATA"]
        path = os.path.join(home, md_dir_name)
    else:       # at least on "linux"
        home = os.environ["HOME"]
        path = os.path.join(home, ".config", md_dir_name)
    return path


# check if we need to transition from SQLite-backed historydict
old_md = None
md_path = get_md_path()
if not os.path.exists(md_path):
    logger.info(
        "New directory to store RE.md between sessions: %s", 
        md_path)
    os.makedirs(md_path)
    from bluesky.utils import get_history
    old_md = get_history()

# Set up a RunEngine and use metadata backed PersistentDict
from bluesky.utils import get_history
RE = RunEngine({})
RE.md = PersistentDict(md_path)
if old_md is not None:
    logger.info("migrating RE.md storage to PersistentDict")
    RE.md.update(old_md)

# keep track of callback subscriptions
callback_db = {}

# Set up a Broker.
from databroker import Broker
db = Broker.named('mongodb_config')

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

# Make plots update live while scans run.
from bluesky.utils import install_kicker
install_kicker()

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
ophyd.EpicsSignal.set_default_timeout(timeout=10, connection_timeout=5)
