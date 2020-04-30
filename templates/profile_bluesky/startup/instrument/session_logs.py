"""
configure session logging
"""

__all__ = ['logger', ]

import logging
import os
import stdlogpj

_log_path = os.path.join(os.getcwd(), ".logs")
if not os.path.exists(_log_path):
    os.mkdir(_log_path)
CONSOLE_IO_FILE = os.path.join(_log_path, "ipython_console.log")

# start logging console to file
# https://ipython.org/ipython-doc/3/interactive/magics.html#magic-logstart
from IPython import get_ipython
_ipython = get_ipython()
# %logstart -o -t .ipython_console.log "rotate"
_ipython.magic(f"logstart -o -t {CONSOLE_IO_FILE} rotate")

BYTE = 1
kB = 1024 * BYTE
MB = 1024 * kB
logger = stdlogpj.standard_logging_setup(
    "bluesky-session", 
    "ipython_logger",
    maxBytes=1*MB, 
    backupCount=9)
logger.setLevel(logging.DEBUG)

logger.info('#'*60 + " startup")
logger.info('logging started')
logger.info(f'logging level = {logger.level}')
