print(__file__)

from ophyd import SingleTrigger, SimDetector
from ophyd import HDF5Plugin, ImagePlugin

class MySingleTriggerHdf5SimDetector(SingleTrigger, SimDetector): 
       
    image = Component(ImagePlugin, suffix="image1:")
    hdf1 = Component(
        HDF5Plugin,
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
except TimeoutError:
    print(f"Could not connect {_ad_prefix} sim detector")
