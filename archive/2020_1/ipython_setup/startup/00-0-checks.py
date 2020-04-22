print(__file__)

import sys
import os

# ensure Python 3.6+

req_version = (3,6)
cur_version = sys.version_info
if cur_version < req_version:
    ver_str = '.'.join((map(str,req_version)))
    msg = 'Requires Python %s+' % ver_str
    msg += ' with BlueSky packages, '
    msg += ' you have ' + sys.version
    msg += '\nfrom directory: ' + sys.prefix
    msg += '\n'*2
    msg += 'You should type `exit` now and find the ipython with BlueSky'
    raise RuntimeError(msg)


# ensure BlueSky is available
try:
    import bluesky
except ImportError:
    msg = 'No module named "bluesky"\n'
    msg += 'This python is from directory: ' + sys.prefix
    msg += '\n'*2
    msg += 'You should type `exit` now and find the ipython with BlueSky'
    raise ImportError(msg)


req_version = (1, 1)
cur_version = tuple(map(int, bluesky.__version__.split(".")[:2]))
if cur_version < req_version:
   ver_str = '.'.join((map(str,req_version)))
   msg = "Need at least BlueSky %s+, " % ver_str
   msg += ' you have ' + bluesky.__version__
   raise ValueError(msg)
print("BlueSky version:", bluesky.__version__)

import ophyd
print("Ophyd version:", ophyd.__version__)
