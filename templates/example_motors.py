
"""
example motors
"""

__all__ = [
    "m1", "m2", "m3", "m4",
    "tth", "th", "chi", "phi",
]

from instrument.session_logs import logger
logger.info(__file__)

from ophyd import EpicsMotor


m1 = EpicsMotor('ioc:m1', name='m1', labels=("motor",))
m2 = EpicsMotor('ioc:m2', name='m2', labels=("motor",))
m3 = EpicsMotor('ioc:m3', name='m3', labels=("motor",))
m4 = EpicsMotor('ioc:m4', name='m4', labels=("motor",))
tth = EpicsMotor('ioc:m5', name='tth', labels=("motor",))
th = EpicsMotor('ioc:m6', name='th', labels=("motor",))
chi = EpicsMotor('ioc:m7', name='chi', labels=("motor",))
phi = EpicsMotor('ioc:m8', name='phi', labels=("motor",))
