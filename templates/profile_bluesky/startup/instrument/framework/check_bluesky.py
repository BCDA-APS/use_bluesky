

import sys

__all__ = []

# ensure BlueSky is available
try:
    import bluesky
except ImportError:
    msg = 'No module named "bluesky"\n'
    msg += 'This python is from directory: ' + sys.prefix
    msg += '\n'*2
    msg += 'You should type `exit` now and find the ipython with Bluesky'
    raise ImportError(msg)


req_version = (1, 6)
cur_version = tuple(map(int, bluesky.__version__.split(".")[:2]))
if cur_version < req_version:
   ver_str = '.'.join((map(str,req_version)))
   msg = "Need at least Bluesky %s+, " % ver_str
   msg += ' you have ' + bluesky.__version__
   raise ValueError(msg)
