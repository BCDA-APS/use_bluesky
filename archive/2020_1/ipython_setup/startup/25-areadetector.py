logger.info(__file__)

"""area detectors: ADSimDetector"""


class MyHDF5Plugin(HDF5Plugin, FileStoreHDF5IterativeWrite):
    create_directory_depth = Component(EpicsSignalWithRBV, suffix="CreateDirectory")


class MySingleTriggerHdf5SimDetector(SingleTrigger, SimDetector): 
       
    image = Component(ImagePlugin, suffix="image1:")
    hdf1 = Component(
        MyHDF5Plugin,
        suffix='HDF1:', 
        root='/',                               # for databroker
        
    # note: path MUST, must, MUST have trailing "/"!!!
    #  ...and... start with the same path defined in root (above)
    write_path_template="/tmp/simdet/%Y/%m/%d/",    # for EPICS AD
    )


_ad_prefix = "xxxSIM1:"		# IOC prefix
try:
    adsimdet = MySingleTriggerHdf5SimDetector(_ad_prefix, name='adsimdet')
    adsimdet.read_attrs.append("hdf1")
    if adsimdet.hdf1.create_directory_depth.value == 0:
        # probably not set, so let's set it now to some default
        adsimdet.hdf1.create_directory_depth.put(-5)
except TimeoutError:
    logger.warning(f"Could not connect {_ad_prefix} sim detector")
