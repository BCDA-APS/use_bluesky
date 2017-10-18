print(__file__)

from ophyd import SingleTrigger, AreaDetector, SimDetector
from ophyd import HDF5Plugin
from ophyd.areadetector.filestore_mixins import FileStoreHDF5IterativeWrite
from ophyd import Component, Device, EpicsSignalWithRBV
from ophyd.areadetector import ADComponent


class MyHDF5Plugin(HDF5Plugin, FileStoreHDF5IterativeWrite):
	
	file_number_sync = None
	
	def get_frames_per_point(self):
		return self.parent.cam.num_images.get()
	

class MyDetector(SingleTrigger, SimDetector):
	
	hdf1 = Component(
		MyHDF5Plugin, 
		"HDF1:", 
		root="/", 					# for databroker filestore
		write_path_template="/tmp",	# for EPICS area detector
		)

try:
	simdet = MyDetector('13SIM1:', name='simdet')
	simdet.read_attrs = ['hdf1', 'cam']
	simdet.hdf1.read_attrs = []  # 'image' gets added dynamically
	#simdet = SimDetector('13SIM1:')
except TimeoutError:
	print("Could not connect 13SIM1: sim detector")

"""
example::

	RE(count([simdet], num=1))
	imgs = db.get_images(db[-1], 'simdet_image')
	imgs[0][0]
	data_uid = simdet.read()['simdet_image']['value']
	fs.retrieve(data_uid)                                                    


	In [15]: %history
	simdet.describe()
	RE(count([simdet]))
	db.get_images(db[-1], 'simdet_image')
	images = _
	images[0]
	images[0][0]
	simdet.cam.num_images.set(2)
	RE(count([simdet]))
	db.get_images(db[-1], 'simdet_image')
	images = _
	images[0][0]
	images[0]
	images[0][1]
	%history


"""
