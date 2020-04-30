
"""
make sure we have the software packages we need
"""

__all__ = []

from ..session_logs import logger
logger.info(__file__)

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
