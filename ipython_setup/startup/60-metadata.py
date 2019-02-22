print(__file__)

from datetime import datetime

# Set up default metadata

RE.md['beamline_id'] = 'developer__YOUR_BEAMLINE_HERE'
RE.md['proposal_id'] = None
RE.md['pid'] = os.getpid()

HOSTNAME = socket.gethostname() or 'localhost' 
USERNAME = getpass.getuser() or 'synApps_xxx_user' 
RE.md['login_id'] = USERNAME + '@' + HOSTNAME
RE.md['BLUESKY_VERSION'] = bluesky.__version__
RE.md['OPHYD_VERSION'] = ophyd.__version__
from apstools import __version__ as apstools_version
RE.md['APSTOOLS_VERSION'] = apstools_version
del apstools_version

print("Metadata dictionary:")
for k, v in sorted(RE.md.items()):
    print("RE.md['%s']" % k, "=", v)
