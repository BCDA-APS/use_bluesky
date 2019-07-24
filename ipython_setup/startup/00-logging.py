print(__file__)

"""
configure logging
"""

LOGGER_FILE = ".ipython_logger.log"
CONSOLE_IO_FILE = ".ipython_console.log"

# start logging console to file
# https://ipython.org/ipython-doc/3/interactive/magics.html#magic-logstart
from IPython import get_ipython
_ipython = get_ipython()
# %logstart -o -t .ipython_console.log "rotate"
_ipython.magic(f"logstart -o -t {CONSOLE_IO_FILE} rotate")


# Uncomment the following lines to turn on 
# verbose messages for debugging.
import logging
#ophyd.logger.setLevel(logging.DEBUG)
#logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(os.path.split(__file__)[-1])
logger = logging.getLogger("bluesky-ipython-shell")
logger.setLevel(logging.DEBUG)

stderr_log_handler = logging.StreamHandler()
logger.addHandler(stderr_log_handler)

# nice output format
# https://docs.python.org/3/library/logging.html#logrecord-attributes
stderr_log_format = "%(levelname)-.1s"		# only first letter
stderr_log_format += " %(asctime)s"
stderr_log_format += " - "
stderr_log_format += "%(message)s"
stderr_log_handler.setFormatter(logging.Formatter(stderr_log_format))
stderr_log_handler.formatter.default_msec_format = "%s.%03d"

file_log_handler = logging.FileHandler(LOGGER_FILE)
logger.addHandler(file_log_handler)
file_log_format = "%(asctime)s"
file_log_format += ",%(levelname)s"
file_log_format += ",%(name)s"
file_log_format += ",%(module)s"
file_log_format += ",%(lineno)d"
file_log_format += ",%(threadName)s"
file_log_format += " - "
file_log_format += "%(message)s"
file_log_handler.setFormatter(logging.Formatter(file_log_format))
file_log_handler.formatter.default_msec_format = "%s.%03d"

logger.warning('#'*60 + " startup")
logger.warning('logging started')
logger.warning(f'logging level = {logger.level}')

# logger.debug('example Debug message')
# logger.info('example Info message')
# logger.warning('example Warning message')
# logger.error('example Error message')
