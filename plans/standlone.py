#!/usr/bin/env python

'''
demonstrate an interlace tomography scan plan in BlueSky

:see: https://github.com/BCDA-APS/use_bluesky/issues/4
'''


#############################################################################
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
os.environ['MDS_HOST'] = 'localhost'
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
'''
ensure that PyEpics is available

Do this early in the setup so other setup can benefit.
'''

import epics
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
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
from ophyd import (EpicsScaler, EpicsSignal, EpicsSignalRO, DeviceStatus)
from ophyd import Component as Cpt

import time

## Beam Monitor Counts
#bs_bm2 = EpicsSignalRO('BL14B:Det:BM2', name='bs_bm2')
noisy = EpicsSignalRO('xxx:userCalc1', name='noisy')
scaler = EpicsScaler('xxx:scaler1', name='scaler')
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
    print(sorted(list(header.keys())))
    start = header.start
    filename = '{}_{}.h5'.format(start.beamline_id, start.scan_id)
    suitcase.nexus.export(header, filename, mds, use_uid=False)
    print('wrote: ' + os.path.abspath(filename))

RE.subscribe('stop', write_nexus_callback)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#############################################################################

import interlace_tomo
