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
import sys
os.environ['EPICS_CA_MAX_ARRAY_BYTES'] = str(EPICS_CA_MAX_ARRAY_BYTES)

import epics

from ophyd import setup_ophyd
setup_ophyd()


# Import matplotlib and put it in interactive mode.
import matplotlib.pyplot as plt
plt.ion()

# Make plots update live while scans run.
from bluesky.utils import install_qt_kicker
install_qt_kicker()

#############################################################################

import socket 
import getpass 


from metadatastore.mds import MDS       #, MDSRO
from filestore.fs import FileStore      #, FileStoreRO
from databroker import Broker

from ophyd import Component as Cpt
from ophyd import Device
from ophyd import Signal
from ophyd import DeviceStatus
from ophyd import PVPositioner
from ophyd import EpicsMotor
from ophyd import EpicsSignal
from ophyd import EpicsSignalRO
from ophyd import PVPositionerPC
from ophyd import EpicsScaler
from ophyd import EpicsSignal
from ophyd import EpicsSignalRO
from ophyd import SingleTrigger
from ophyd import AreaDetector
from ophyd import SimDetector
from ophyd import HDF5Plugin
from ophyd import TIFFPlugin
from ophyd import DynamicDeviceComponent as DDCpt

from ophyd.areadetector.filestore_mixins import FileStoreHDF5IterativeWrite
from ophyd.areadetector.filestore_mixins import FileStoreTIFFIterativeWrite
from ophyd.areadetector import ADComponent as ADCpt
from ophyd.areadetector import EpicsSignalWithRBV
from ophyd.areadetector import ImagePlugin
from ophyd.areadetector import StatsPlugin
from ophyd.areadetector import DetectorBase
from ophyd.areadetector import ROIPlugin
from ophyd.areadetector import ProcessPlugin
from ophyd.areadetector import TransformPlugin

from bluesky.global_state import gs
from bluesky.callbacks import LiveTable

import suitcase.nexus

#############################################################################


# class myHDF5Plugin(HDF5Plugin):
#  
#     array_callbacks = Cpt(EpicsSignalWithRBV, 'ArrayCallbacks')
#     enable_callbacks = Cpt(EpicsSignalWithRBV, 'EnableCallbacks')
#     auto_increment = Cpt(EpicsSignalWithRBV, 'AutoIncrement')
#     auto_save = Cpt(EpicsSignalWithRBV, 'AutoSave')
#     file_path = Cpt(EpicsSignalWithRBV, 'FilePath', string=True)
#     file_name = Cpt(EpicsSignalWithRBV, 'FileName', string=True)
#     file_number = Cpt(EpicsSignalWithRBV, 'FileNumber')
#     file_template = Cpt(EpicsSignalWithRBV, 'FileTemplate', string=True)
#     file_write_mode = Cpt(EpicsSignalWithRBV, 'FileWriteMode')
#     full_file_name = Cpt(EpicsSignalRO, 'FullFileName_RBV', string=True)
#     xml_layout_file = Cpt(EpicsSignalWithRBV, 'XMLFileName', string=True)


class MyDetector(SingleTrigger, SimDetector):

    no_op = None
    # image1 = Cpt(ImagePlugin, 'image1:')
    # hdf1 = Cpt(myHDF5Plugin, 'HDF1:')


def setup_sim_detector(det):
    # assume sim detector is unconfigured, apply all config here
    cam = det.cam

    cam.acquire_time.put(0.5)    # seconds
    cam.array_callbacks.put("Enable")
    cam.data_type.put("UInt8")
    cam.image_mode.put(0) # Single
    cam.num_exposures.put(1)
    cam.num_images.put(1)
    cam.shutter_mode.put("None")
    cam.trigger_mode.put("Internal")
    # specific to sim detector
    cam.sim_mode.put("LinearRamp")
    
    if hasattr(det, 'hdf1'):
        hdf = det.hdf1
    
        hdf.array_callbacks.put('Enable')
        hdf.auto_increment.put('Yes')
        hdf.auto_save.put('Yes')
        hdf.enable_callbacks.put('Enable')
        hdf.file_path.put(os.getcwd())  # TODO: get from EPICS PV
        hdf.file_name.put('tomoscan')   # TODO: get from EPICS PV
        hdf.file_template.put('%s%s_%5.5d.h5')
        hdf.file_write_mode.put('Single')
        # hdf.xml_layout_file.put('')    # won't work for empty strings, but why?


def print_scan_ids(name, start_doc):
    """callback that prints scan IDs at the start of each scan"""
    print("Transient Scan ID: {0}".format(start_doc['scan_id']))
    print("Persistent Unique Scan ID: '{0}'".format(start_doc['uid']))


class EpicsNotice(Device):
    '''
    progress messages posted to a couple stringout PVs
    '''
 
    msg_a = Cpt(EpicsSignal, 'userStringCalc1.AA')
    msg_b = Cpt(EpicsSignal, 'userStringCalc1.BB')
    
    def post(self, a=None, b=None):
        """write text to each/either PV"""
        if a is not None:
            self.msg_a.put(str(a))
        if b is not None:
            self.msg_b.put(str(b))


#############################################################################


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

mds = MDS(mds_config)
fs = FileStore(fs_config)
db = Broker(mds, fs)

RE = gs.RE  # convenience alias
RE.subscribe('all', mds.insert)


alpha = EpicsMotor(SYNAPPS_IOC_PREFIX + 'm1', name='alpha')
beta = EpicsMotor(SYNAPPS_IOC_PREFIX + 'm2', name='beta')
gamma = EpicsMotor(SYNAPPS_IOC_PREFIX + 'm3', name='gamma')
x = EpicsMotor(SYNAPPS_IOC_PREFIX + 'm4', name='x')
y = EpicsMotor(SYNAPPS_IOC_PREFIX + 'm5', name='y')
z = EpicsMotor(SYNAPPS_IOC_PREFIX + 'm6', name='z')

noisy = EpicsSignalRO(SYNAPPS_IOC_PREFIX + 'userCalc1', name='noisy')
scaler = EpicsScaler(SYNAPPS_IOC_PREFIX + 'scaler1', name='scaler')


simdet = MyDetector(AD_IOC_PREFIX)
setup_sim_detector(simdet)


RE.md['beamline_id'] = 'developer'
RE.md['proposal_id'] = None
RE.md['pid'] = os.getpid()


RE.subscribe('start', print_scan_ids)


HOSTNAME = socket.gethostname() or 'localhost' 
USERNAME = getpass.getuser() or 'synApps_xxx_user' 
RE.md['login_id'] = USERNAME + '@' + HOSTNAME


epics_string_notices = EpicsNotice(SYNAPPS_IOC_PREFIX, name='messages')
epics_string_notices.post()



#############################################################################

if __name__ == '__main__':
    import interlace_tomo
    
    tomo_callbacks = []
    detectors = [scaler,]
    prescan_checks = interlace_tomo.PreTomoScanChecks(alpha, source_intensity=None)
    live_table = LiveTable([alpha, beta, scaler.time, scaler.channels.chan1, scaler.channels.chan2])
    epics_notifier = interlace_tomo.EPICSNotifierCallback(epics_string_notices)
    
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

    fn = interlace_tomo.FrameNotifier(path='/home/prjemian/Documents')
    tomo_callbacks.append(fn)
    
    # TODO: How to get frame file name into event document?
    # TODO: How to get frame file names into LiveTable?

    tomo_plan = interlace_tomo.interlace_tomo_scan(detectors, alpha, 1, 2, 5, 5, snake=True)
    RE(tomo_plan, tomo_callbacks, md=dict(developer=True))
