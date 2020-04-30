
"""
APS only: connect with facility information
"""

__all__ = [
    'aps', 
    # 'undulator',
    ]

from ..session_logs import logger
logger.info(__file__)

import apstools.devices

from ..framework import sd

class MyApsDevice(apstools.devices.ApsMachineParametersDevice):
    # for local modifications
    pass

aps = MyApsDevice(name="aps")
sd.baseline.append(aps)

# TODO: insertion device?
# Cannot connect with either of these.
# # apstools.devices.ApsUndulator
# # apstools.devices.ApsUndulatorDual
# class MyUndulatorDevice(apstools.devices.ApsUndulatorDual):
#     # for local modifications
#     pass

# undulator = MyUndulatorDevice("ID29", name="undulator")
# sd.baseline.append(undulator)
