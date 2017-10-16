print(__file__)

'''
write every scan to a NeXus file

file: 95_write_NeXus_when_stop.py

When a `stop` document is received, write the most recent scan 
to a NeXus HDF5 file.
'''
# 2017-10-16,prj: suitcase.nexus is out of date, remove for now

### import suitcase.nexus
### import os
###
###
### def write_nexus_callback(name, stop_doc):
###	# name == 'stop'
###	# stop_doc is db[-1]['stop']
###	if name != 'stop':
###	    return
###	header = db[stop_doc['run_start']]
###	print(sorted(list(header.keys())))
###	start = header.start
###	filename = '{}_{}.h5'.format(start.beamline_id, start.scan_id)
###	suitcase.nexus.export(header, filename, mds, use_uid=False)
###	print('wrote: ' + os.path.abspath(filename))
###
### RE.subscribe('stop', write_nexus_callback)
### # RE(scan([noisy], m1, -1, 1, 3), LiveTable([noisy, m1]))
### # write_nexus_callback('stop', db[-1]['stop'])
