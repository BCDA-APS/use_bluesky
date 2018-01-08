print(__file__)

import sys
import os

# ensure Python 3.6+

req_version = (3,6)
cur_version = sys.version_info
if cur_version < req_version:
    msg = 'Requires Python %s+' % '.'.join(req_version)
    msg += ' with BlueSky packages\n'
    msg += 'found: ' + sys.version
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


_major, _minor,  = map(int, bluesky.__version__.split(".")[:2])
if _major == 1:
    if _minor < 0:
       msg = "Need at least BlueSky 1.0+ you have "
       msg += bluesky.__version__
       raise ValueError(msg)
print("BlueSky version:", bluesky.__version__)
