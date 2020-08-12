
"""
example motors
"""

# examples are commented out

# __all__ = [
#     "m1", "m2", "m3", "m4",
#     "tth", "th", "chi", "phi",
# ]

from instrument.session_logs import logger
logger.info(__file__)

from ophyd import EpicsMotor

# # the ``labels``` adds each motor to the ``wa motor`` command.
# # add other such grouping labels as desired, such as "diffractometer"

# m1 = EpicsMotor('ioc:m1', name='m1', labels=("motor",))
# m2 = EpicsMotor('ioc:m2', name='m2', labels=("motor",))
# m3 = EpicsMotor('ioc:m3', name='m3', labels=("motor",))
# m4 = EpicsMotor('ioc:m4', name='m4', labels=("motor",))
# tth = EpicsMotor('ioc:m5', name='tth', labels=("motor", "diffractometer"))
# th = EpicsMotor('ioc:m6', name='th', labels=("motor", "diffractometer"))
# chi = EpicsMotor('ioc:m7', name='chi', labels=("motor", "diffractometer"))
# phi = EpicsMotor('ioc:m8', name='phi', labels=("motor", "diffractometer"))
