
"""
devices and functions that support interlaced tomography scanning
"""


import os
import ophyd


class myHDF5Plugin(ophyd.Device):
    """custom handling of the HDF5 file writing plugin"""
    # NOTE: ophyd.areadetector.HDF5Plugin needs testing with AD2.6, use Device for now
  
    array_callbacks = ophyd.Component(ophyd.EpicsSignalWithRBV, 'ArrayCallbacks')
    enable_callbacks = ophyd.Component(ophyd.EpicsSignalWithRBV, 'EnableCallbacks')
    auto_increment = ophyd.Component(ophyd.EpicsSignalWithRBV, 'AutoIncrement')
    auto_save = ophyd.Component(ophyd.EpicsSignalWithRBV, 'AutoSave')
    file_path = ophyd.Component(ophyd.EpicsSignalWithRBV, 'FilePath', string=True)
    file_name = ophyd.Component(ophyd.EpicsSignalWithRBV, 'FileName', string=True)
    file_number = ophyd.Component(ophyd.EpicsSignalWithRBV, 'FileNumber')
    file_template = ophyd.Component(ophyd.EpicsSignalWithRBV, 'FileTemplate', string=True)
    file_write_mode = ophyd.Component(ophyd.EpicsSignalWithRBV, 'FileWriteMode')
    full_file_name = ophyd.Component(ophyd.EpicsSignalRO, 'FullFileName_RBV', string=True)
    store_attributes = ophyd.Component(ophyd.EpicsSignalWithRBV, 'StoreAttr', string=True)
    store_performance_data = ophyd.Component(ophyd.EpicsSignalWithRBV, 'StorePerform', string=True)
    xml_layout_file = ophyd.Component(ophyd.EpicsSignalWithRBV, 'XMLFileName', string=True)


class MyDetector(ophyd.SingleTrigger, ophyd.SimDetector):
    """customize the sim detector handling"""
    #  NOTE: ophyd.areadetector.ImagePlugin needs testing with AD2.6

    no_op = None
    # image1 = ophyd.Component(ImagePlugin, 'image1:')
    hdf1 = ophyd.Component(myHDF5Plugin, 'HDF1:')


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
        hdf.store_attributes.put("Yes")
        hdf.store_performance_data.put("No")
        # hdf.xml_layout_file.put('')    # won't work for empty strings, but why?


def print_scan_ids(name, start_doc):
    """callback that prints scan IDs at the start of each scan"""
    print("Transient Scan ID: {0}".format(start_doc['scan_id']))
    print("Persistent Unique Scan ID: '{0}'".format(start_doc['uid']))


class EpicsNotice(ophyd.Device):
    '''
    progress messages posted to a couple stringout PVs
    '''
 
    msg_a = ophyd.Component(ophyd.EpicsSignal, 'userStringCalc1.AA')
    msg_b = ophyd.Component(ophyd.EpicsSignal, 'userStringCalc1.BB')
    
    def post(self, a=None, b=None):
        """write text to each/either PV"""
        if a is not None:
            self.msg_a.put(str(a)[:39])
        if b is not None:
            self.msg_b.put(str(b)[:39])
