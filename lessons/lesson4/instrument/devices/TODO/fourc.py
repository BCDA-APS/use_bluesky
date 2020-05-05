
"""
Four circle diffractometer
"""

__all__ = [
    "fourc",
    ]

from ..session_logs import logger
logger.info(__file__)

import gi
gi.require_version('Hkl', '5.0')
from hkl.diffract import E4CV, E4CH  #this works for mu=0
from hkl.util import Lattice

from bluesky import plans as bp
from bluesky import plan_stubs as bps

from ophyd import Component
from ophyd import EpicsMotor
from ophyd import PseudoSingle
from ophyd import SoftPositioner

from .diffractometer import AxisConstraints
from .diffractometer import DiffractometerMixin

# TODO: pick the motors at 29-ID
MOTOR_PV_OMEGA = "sky:m9"
MOTOR_PV_CHI = "sky:m10"
MOTOR_PV_PHI = "sky:m11"
MOTOR_PV_TTH = "sky:m12"


class FourCircleDiffractometer(DiffractometerMixin, E4CV):
    h = Component(PseudoSingle, '', labels=("hkl", "fourc"))
    k = Component(PseudoSingle, '', labels=("hkl", "fourc"))
    l = Component(PseudoSingle, '', labels=("hkl", "fourc"))

    omega = Component(EpicsMotor, MOTOR_PV_OMEGA, labels=("motor", "fourc"))
    chi =   Component(EpicsMotor, MOTOR_PV_CHI, labels=("motor", "fourc"))
    phi =   Component(EpicsMotor, MOTOR_PV_PHI, labels=("motor", "fourc"))
    tth =   Component(EpicsMotor, MOTOR_PV_TTH, labels=("motor", "fourc"))

fourc = FourCircleDiffractometer('', name='fourc')
logger.info(f"{fourc.name} modes: {fourc.engine.modes}")
fourc.calc.engine.mode = fourc.engine.modes[0]  # 'bissector' - constrain tth = 2 * omega
logger.info(f"selected mode: {fourc.calc.engine.mode}")


# this is an example:
# # reflections = [(h-2,k-2,l-2) for h in range(5) for k in range(5) for l in range(5)]
# reflections = (
#     (1,0,0), 
#     (1,1,0), 
#     (1,0,1), 
#     (1,1,1),
# )
# logger.info(fourc.forwardSolutionsTable(reflections, full=True))
