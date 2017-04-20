#!/usr/bin/env python

'''
setup a standalone global state to run one interlace tomography scan plan in BlueSky

:see: https://github.com/BCDA-APS/use_bluesky/issues/4
'''

MONGODB_HOST = 'localhost'
EPICS_CA_MAX_ARRAY_BYTES=10000000
AD_IOC_PREFIX = '13SIM1:'
SYNAPPS_IOC_PREFIX = 'xxx:'

#############################################################################

# these things must import and set first, then other imports
import os
os.environ['EPICS_CA_MAX_ARRAY_BYTES'] = str(EPICS_CA_MAX_ARRAY_BYTES)

from ophyd import setup_ophyd
setup_ophyd()


# Import matplotlib and put it in interactive mode.
import matplotlib.pyplot as plt
plt.ion()

# Make plots update live while scans run.
from bluesky.utils import install_qt_kicker
install_qt_kicker()

#############################################################################

import logging
import socket 
import getpass 

import filestore.fs
import metadatastore.mds
import databroker

import ophyd
import bluesky.global_state, bluesky.callbacks
import suitcase

import my_devices
import interlace_tomo


#############################################################################

if __name__ == '__main__':

    logging.basicConfig()
    logger = logging.getLogger()
    logger.info('starting: ' + __file__)
    
    os.environ['MDS_HOST'] = MONGODB_HOST
    os.environ['MDS_PORT'] = '27017'
    os.environ['MDS_DATABASE'] = 'metadatastore-production-v1'
    os.environ['MDS_TIMEZONE'] = 'US/Central'
    os.environ['FS_HOST'] = os.environ['MDS_HOST']
    os.environ['FS_PORT'] = os.environ['MDS_PORT']
    os.environ['FS_DATABASE'] = 'filestore-production-v1'
    
    # Connect to metadatastore and filestore.
    mds_config = {'host': os.environ['MDS_HOST'],
                  'port': int(os.environ['MDS_PORT']),
                  'database': os.environ['MDS_DATABASE'],
                  'timezone': os.environ['MDS_TIMEZONE']}
    fs_config = {'host': os.environ['FS_HOST'],
                 'port': int(os.environ['FS_PORT']),
                 'database': os.environ['FS_DATABASE']}
    
    mds = metadatastore.mds.MDS(mds_config)
    fs = filestore.fs.FileStore(fs_config)
    db = databroker.Broker(mds, fs)
    
    RE = bluesky.global_state.gs.RE  # convenience alias
    RE.subscribe('all', mds.insert)
    
    
    alpha = ophyd.EpicsMotor(SYNAPPS_IOC_PREFIX + 'm1', name='alpha')
    beta = ophyd.EpicsMotor(SYNAPPS_IOC_PREFIX + 'm2', name='beta')
    gamma = ophyd.EpicsMotor(SYNAPPS_IOC_PREFIX + 'm3', name='gamma')
    x = ophyd.EpicsMotor(SYNAPPS_IOC_PREFIX + 'm4', name='x')
    y = ophyd.EpicsMotor(SYNAPPS_IOC_PREFIX + 'm5', name='y')
    z = ophyd.EpicsMotor(SYNAPPS_IOC_PREFIX + 'm6', name='z')
    
    noisy = ophyd.EpicsSignalRO(SYNAPPS_IOC_PREFIX + 'userCalc1', name='noisy')
    scaler = ophyd.EpicsScaler(SYNAPPS_IOC_PREFIX + 'scaler1', name='scaler')
    
    
    simdet = my_devices.MyDetector(AD_IOC_PREFIX)
    my_devices.setup_sim_detector(simdet)
    
    
    RE.md['beamline_id'] = 'developer'
    RE.md['proposal_id'] = None
    RE.md['pid'] = os.getpid()
    
    
    RE.subscribe('start', my_devices.print_scan_ids)
    
    
    HOSTNAME = socket.gethostname() or 'localhost' 
    USERNAME = getpass.getuser() or 'synApps_xxx_user' 
    RE.md['login_id'] = USERNAME + '@' + HOSTNAME
    
    
    epics_string_notices = my_devices.EpicsNotice(SYNAPPS_IOC_PREFIX, name='messages')
    epics_string_notices.post()

    tomo_callbacks = []
    detectors = [scaler,]
    prescan_checks = interlace_tomo.PreTomoScanChecks(alpha, source_intensity=None)
    live_table = bluesky.callbacks.LiveTable([alpha, beta, scaler.time, scaler.channels.chan1, scaler.channels.chan2])
    epics_notifier = interlace_tomo.EPICSNotifierCallback(epics_string_notices)
    live_plot = bluesky.callbacks.LivePlot('noisy', 'alpha_user_setpoint', marker='x', color='red', linestyle='None')
    
    detectors = [simdet, noisy]
    live_table_signals = [alpha, beta]
    live_table = bluesky.callbacks.LiveTable(live_table_signals)

    tomo_callbacks.append(prescan_checks)
    tomo_callbacks.append(live_table)
    tomo_callbacks.append(epics_notifier)
    tomo_callbacks.append(live_plot)
    
    hdf_xface = None
    if hasattr(simdet, 'hdf1'):
        hdf_xface = simdet.hdf1
    fn = interlace_tomo.FrameNotifier(path='/home/prjemian/Documents', hdf=hdf_xface)
    tomo_callbacks.append(fn)
    
    # TODO: How to get frame file names into LiveTable?
    start_angle = 0
    end_angle = 10
    num_projections_inner = 10
    num_divisions_outer = 16

    simdet.cam.acquire_time.put(0.01)    # seconds
    tomo_plan = interlace_tomo.interlace_tomo_scan(
        detectors, alpha, 
        start_angle, 
        end_angle, 
        num_projections_inner, 
        num_divisions_outer, 
        snake=True, 
        bisection=True)
    RE(tomo_plan, tomo_callbacks, md=dict(developer=True))
