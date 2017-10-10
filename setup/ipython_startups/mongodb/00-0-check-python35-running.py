print(__file__)
# ensure Python 3.5+
import sys
req_version = (3,5)
cur_version = sys.version_info
if cur_version < req_version:
    msg = 'Requires Python 3.5+ with BlueSky packages\n'
    msg += 'found: ' + sys.version
    msg += '\nfrom directory: ' + sys.prefix
    msg += '\n'*2
    msg += 'You should type `exit` now and find the ipython with BlueSky'
    raise RuntimeError(msg)
