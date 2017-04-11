#!/usr/bin/env python

'''
setup s standalone global state to run an interlace tomography scan plan in BlueSky

:see: https://github.com/BCDA-APS/use_bluesky/issues/4
'''
MONGODB_HOST = 'localhost'

#############################################################################
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
from ophyd.commands import *
from bluesky.callbacks import *
from bluesky.spec_api import *
from bluesky.global_state import gs, abort, stop, resume
from bluesky.plan_tools import print_summary
from time import sleep
import numpy as np
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# set up the data broker (db)

import os

# this *should* come from ~/.config/filestore and ~/.config/metadatastore
os.environ['MDS_HOST'] = MONGODB_HOST
os.environ['MDS_PORT'] = '27017'
os.environ['MDS_DATABASE'] = 'metadatastore-production-v1'
os.environ['MDS_TIMEZONE'] = 'US/Central'
os.environ['FS_HOST'] = os.environ['MDS_HOST']
os.environ['FS_PORT'] = os.environ['MDS_PORT']
os.environ['FS_DATABASE'] = 'filestore-production-v1'

# Connect to metadatastore and filestore.
from metadatastore.mds import MDS, MDSRO
from filestore.fs import FileStore, FileStoreRO
from databroker import Broker
mds_config = {'host': os.environ['MDS_HOST'],
              'port': int(os.environ['MDS_PORT']),
              'database': os.environ['MDS_DATABASE'],
              'timezone': os.environ['MDS_TIMEZONE']}
fs_config = {'host': os.environ['FS_HOST'],
             'port': int(os.environ['FS_PORT']),
             'database': os.environ['FS_DATABASE']}
mds = MDS(mds_config)
# For code that only reads the databases, use the readonly version
#mds_readonly = MDSRO(mds_config)
#fs_readonly = FileStoreRO(fs_config)
fs = FileStore(fs_config)
db = Broker(mds, fs)

# Subscribe metadatastore to documents.
# If this is removed, data is not saved to metadatastore.
from bluesky.global_state import gs
gs.RE.subscribe('all', mds.insert)
RE = gs.RE  # convenience alias
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ensure that PyEpics is available
# Do this early in the setup so other setup can benefit.
import epics
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# setup the movables
from ophyd import (PVPositioner, EpicsMotor, EpicsSignal, EpicsSignalRO,
                   PVPositionerPC, Device)
from ophyd import Component as Cpt

alpha = EpicsMotor('xxx:m1', name='alpha')
beta = EpicsMotor('xxx:m2', name='beta')
gamma = EpicsMotor('xxx:m3', name='gamma')
x = EpicsMotor('xxx:m4', name='x')
y = EpicsMotor('xxx:m5', name='y')
z = EpicsMotor('xxx:m6', name='z')
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# setup the detectors
from ophyd import (EpicsScaler, EpicsSignal, EpicsSignalRO, DeviceStatus)
from ophyd import Component as Cpt

import time

## Beam Monitor Counts
#bs_bm2 = EpicsSignalRO('BL14B:Det:BM2', name='bs_bm2')
noisy = EpicsSignalRO('xxx:userCalc1', name='noisy')
scaler = EpicsScaler('xxx:scaler1', name='scaler')
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from ophyd import SingleTrigger, AreaDetector, SimDetector

class MyDetector(SingleTrigger, SimDetector): pass

ad_prefix = '13SIM1:'
simdet = MyDetector(ad_prefix)
# assume sim detector is unconfigured, apply all config here
simdet.cam.acquire_time.put(0.5)    # seconds
simdet.cam.array_callbacks.put("Enable")
simdet.cam.data_type.put("UInt8")
simdet.cam.image_mode.put("Single")
simdet.cam.num_exposures.put(1)
simdet.cam.num_images.put(1)
simdet.cam.shutter_mode.put("None")
simdet.cam.trigger_mode.put("Internal")
# specific to sim detector
simdet.cam.sim_mode.put("LinearRamp")
# how to configure these plugins using ophyd?  use PyEpics for now
hdf5_prefix = simdet.name + 'HDF1:'
epics.caput(hdf5_prefix + 'EnableCallbacks', 'Enable')
epics.caput(hdf5_prefix + 'ArrayCallbacks', 'Enable')
epics.caput(hdf5_prefix + 'FilePath', os.getcwd())  # TODO: get from EPICS PV
epics.caput(hdf5_prefix + 'FileName', 'tomoscan')   # TODO: get from EPICS PV
epics.caput(hdf5_prefix + 'AutoIncrement', 'Yes')
epics.caput(hdf5_prefix + 'FileTemplate', '%s%s_%5.5d.h5')
epics.caput(hdf5_prefix + 'AutoSave', 'Yes')
epics.caput(hdf5_prefix + 'FileWriteMode', 'Single')
hdf5_frame_file = EpicsSignalRO(hdf5_prefix + 'FullFileName_RBV', name='hdf5_frame_file')
#epics.caput(hdf5_prefix + 'XMLFileName', '')    # name of layout template
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Set up default metadata
RE.md['beamline_id'] = 'developer'
RE.md['proposal_id'] = None
RE.md['pid'] = os.getpid()

# Add a callback that prints scan IDs at the start of each scan.

def print_scan_ids(name, start_doc):
    print("Transient Scan ID: {0}".format(start_doc['scan_id']))
    print("Persistent Unique Scan ID: '{0}'".format(start_doc['uid']))

gs.RE.subscribe('start', print_scan_ids)

import socket 
import getpass 
HOSTNAME = socket.gethostname() or 'localhost' 
USERNAME = getpass.getuser() or 'synApps_xxx_user' 
gs.RE.md['login_id'] = USERNAME + '@' + HOSTNAME
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''
write every scan to a NeXus file

file: 95_write_NeXus_when_stop.py

When a `stop` document is received, write the most recent scan 
to a NeXus HDF5 file.
'''

import suitcase.nexus
import os


def write_nexus_callback(name, stop_doc):
    # name == 'stop'
    # stop_doc is db[-1]['stop']
    if name != 'stop':
        return
    header = db[stop_doc['run_start']]
    #print(sorted(list(header.keys())))
    start = header.start
    filename = '{}_{}.h5'.format(start.beamline_id, start.scan_id)
    suitcase.nexus.export(header, filename, mds, use_uid=False)
    print('wrote: ' + os.path.abspath(filename))

# FIXME: fails with area detector
#RE.subscribe('stop', write_nexus_callback)
"""
Traceback (most recent call last):
  File "/home/prjemian/Documents/eclipse/use_bluesky/plans/standlone.py", line 205, in <module>
    RE(tomo_plan, tomo_callbacks, md=dict(developer=True))
  File "/home/prjemian/Apps/BlueSky/lib/python3.5/site-packages/bluesky/run_engine.py", line 599, in __call__
    raise exc
  File "/home/prjemian/Apps/BlueSky/lib/python3.5/asyncio/tasks.py", line 239, in _step
    result = coro.send(None)
  File "/home/prjemian/Apps/BlueSky/lib/python3.5/site-packages/bluesky/run_engine.py", line 1007, in _run
    raise err
  File "/home/prjemian/Apps/BlueSky/lib/python3.5/site-packages/bluesky/run_engine.py", line 905, in _run
    msg = self._plan_stack[-1].send(resp)
  File "/home/prjemian/Documents/eclipse/use_bluesky/plans/interlace_tomo.py", line 172, in interlace_tomo_scan
    return (yield from inner_scan())
  File "/home/prjemian/Apps/BlueSky/lib/python3.5/site-packages/bluesky/plans.py", line 47, in dec_inner
    return (yield from plan)
  File "/home/prjemian/Apps/BlueSky/lib/python3.5/site-packages/bluesky/plans.py", line 1510, in stage_wrapper
    return (yield from finalize_wrapper(inner(), unstage_devices()))
  File "/home/prjemian/Apps/BlueSky/lib/python3.5/site-packages/bluesky/plans.py", line 1025, in finalize_wrapper
    ret = yield from plan
  File "/home/prjemian/Apps/BlueSky/lib/python3.5/site-packages/bluesky/plans.py", line 1508, in inner
    return (yield from plan)
  File "/home/prjemian/Apps/BlueSky/lib/python3.5/site-packages/bluesky/plans.py", line 47, in dec_inner
    return (yield from plan)
  File "/home/prjemian/Apps/BlueSky/lib/python3.5/site-packages/bluesky/plans.py", line 874, in run_wrapper
    rs_uid = yield from close_run()
  File "/home/prjemian/Apps/BlueSky/lib/python3.5/site-packages/bluesky/plans.py", line 967, in close_run
    return (yield Msg('close_run'))
  File "/home/prjemian/Apps/BlueSky/lib/python3.5/site-packages/bluesky/run_engine.py", line 956, in _run
    response = yield from coro(msg)
  File "/home/prjemian/Apps/BlueSky/lib/python3.5/site-packages/bluesky/run_engine.py", line 1211, in _close_run
    yield from self.emit(DocumentNames.stop, doc)
  File "/home/prjemian/Apps/BlueSky/lib/python3.5/asyncio/coroutines.py", line 206, in coro
    res = func(*args, **kw)
  File "/home/prjemian/Apps/BlueSky/lib/python3.5/site-packages/bluesky/run_engine.py", line 1969, in emit
    self.dispatcher.process(name, doc)
  File "/home/prjemian/Apps/BlueSky/lib/python3.5/site-packages/bluesky/run_engine.py", line 1981, in process
    exceptions = self.cb_registry.process(name, name.name, doc)
  File "/home/prjemian/Apps/BlueSky/lib/python3.5/site-packages/bluesky/utils.py", line 271, in process
    func(*args, **kwargs)
  File "/home/prjemian/Apps/BlueSky/lib/python3.5/site-packages/bluesky/utils.py", line 352, in __call__
    return mtd(*args, **kwargs)
  File "/home/prjemian/Documents/eclipse/use_bluesky/plans/standlone.py", line 170, in write_nexus_callback
    suitcase.nexus.export(header, filename, mds, use_uid=False)
  File "/home/prjemian/Apps/BlueSky/lib/python3.5/site-packages/suitcase/nexus.py", line 178, in export
    timestamps = [e['timestamps'][safename] for e in events]
  File "/home/prjemian/Apps/BlueSky/lib/python3.5/site-packages/suitcase/nexus.py", line 178, in <listcomp>
    timestamps = [e['timestamps'][safename] for e in events]
KeyError: '_13SIM1__cam_peak_start_peak_start_y'
"""
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#############################################################################

if __name__ == '__main__':
    import interlace_tomo
    
    tomo_callbacks = []
    detectors = [scaler,]
    prescan_checks = interlace_tomo.PreTomoScanChecks(alpha)
    live_table = LiveTable([alpha, beta, scaler.time, scaler.channels.chan1, scaler.channels.chan2])
    epics_notifier = interlace_tomo.EPICSNotifierCallback("xxx:userStringCalc1.AA", "xxx:userStringCalc1.BB")
    
    detectors = [simdet]
    live_table = LiveTable([alpha, beta])

    tomo_callbacks.append(prescan_checks)
    tomo_callbacks.append(live_table)
    tomo_callbacks.append(epics_notifier)
    
    #plan = interlace_tomo.tomo_scan(detectors, alpha, 1.0, 2.0, 5)
    #RE(plan, callbacks, md=dict(developer=True))
    
    # tomo_plan = interlace_tomo.interlace_tomo_scan(detectors, alpha, 1, 2, 5, 5, snake=True)
    # RE(tomo_plan, tomo_callbacks, md=dict(developer=True))
    # 
    # tomo_plan = interlace_tomo.interlace_tomo_scan(detectors, alpha, 0.8, 0.0, 5, 4)
    # RE(tomo_plan, tomo_callbacks, md=dict(developer=True))

    fn = interlace_tomo.FrameNotifier(simdet, path='/home/prjemian/Documents')
    tomo_callbacks.append(fn)
    
    # TODO: How to get frame file name into event document?
    # TODO: How to get frame file names into LiveTable?

    tomo_plan = interlace_tomo.interlace_tomo_scan(detectors, alpha, 1, 2, 5, 5, snake=True)
    RE(tomo_plan, tomo_callbacks, md=dict(developer=True))
