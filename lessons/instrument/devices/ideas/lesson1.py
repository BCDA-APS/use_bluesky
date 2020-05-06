
"""
lesson 1 : create the scaler
"""

__all__ = [
    'scaler', 
    # 'undulator',
    ]

from ...session_logs import logger
logger.info(__file__)

from apstools.devices import use_EPICS_scaler_channels
from ophyd.scaler import ScalerCH

scaler = ScalerCH("sky:scaler1", name="scaler")

scaler.wait_for_connection()
scaler.match_names()
use_EPICS_scaler_channels(scaler)
