
"""
lesson 2 : create the motor and scaler
"""

__all__ = [
    'm1',
    'scaler', 
    ]

from ...session_logs import logger
logger.info(__file__)

from apstools.devices import use_EPICS_scaler_channels
from ophyd import EpicsMotor
from ophyd.scaler import ScalerCH

m1 = EpicsMotor("sky:m1", name="m1")
scaler = ScalerCH("sky:scaler1", name="scaler")

m1.wait_for_connection()
scaler.wait_for_connection()

scaler.match_names()
use_EPICS_scaler_channels(scaler)
