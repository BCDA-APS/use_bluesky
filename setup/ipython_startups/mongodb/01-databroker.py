print(__file__)
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


