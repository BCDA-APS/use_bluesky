
"""
lesson 3 : create the motor and scaler
"""

__all__ = [
    'm1',
    'scaler', 
    ]

from ...session_logs import logger
logger.info(__file__)

from ophyd import EpicsMotor
from ophyd.scaler import ScalerCH

P = "sky:"
m1 = EpicsMotor(f"{P}m1", name="m1")
scaler = ScalerCH(f"{P}scaler1", name="scaler")

m1.wait_for_connection()
scaler.wait_for_connection()

scaler.select_channels(None)
