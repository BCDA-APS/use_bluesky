print(__file__)
import sys

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
if _major == 0:
    if _minor < 10:
       msg = "Need at least BlueSky version >= 0.10, you have "
       msg += bluesky.__version__
       raise ValueError(msg)
