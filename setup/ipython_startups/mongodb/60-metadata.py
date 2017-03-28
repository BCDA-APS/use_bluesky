
# Set up default metadata

RE.md['beamline_id'] = 'developer'
RE.md['proposal_id'] = None

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

import os
for key, value in os.environ.items():
	if key.startswith("EPICS"):
		gs.RE.md[key] = value
