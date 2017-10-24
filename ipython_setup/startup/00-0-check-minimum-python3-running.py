print(__file__)

import sys
import os

# ensure Python 3.6+

req_version = (3,6)
cur_version = sys.version_info
if cur_version < req_version:
    msg = 'Requires Python 3.6+ with BlueSky packages\n'
    msg += 'found: ' + sys.version
    msg += '\nfrom directory: ' + sys.prefix
    msg += '\n'*2
    msg += 'You should type `exit` now and find the ipython with BlueSky'
    raise RuntimeError(msg)
