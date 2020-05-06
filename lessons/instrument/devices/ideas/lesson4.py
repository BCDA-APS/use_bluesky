
"""
lesson 4 : get motor and scaler from ophyd simulators
"""

__all__ = [
    'm1',
    'scaler', 
    ]

from ...session_logs import logger
logger.info(__file__)

from ophyd.sim import motor as m1
from ophyd.sim import det as scaler
