#!/APSshare/anaconda3/BlueSky/bin/python

"lesson 3: Show the data as it is acquired"

from ophyd import EpicsMotor
from ophyd.scaler import ScalerCH
from bluesky import RunEngine
import bluesky.plans as bp
from bluesky.callbacks import LiveTable
from bluesky.callbacks import LivePlot
from bluesky.callbacks.best_effort import BestEffortCallback
from APS_BlueSky_tools.devices import use_EPICS_scaler_channels


%matplotlib notebook
from bluesky.utils import install_qt_kicker
install_qt_kicker()


RE = RunEngine({})
m1 = EpicsMotor("prj:m1", name="m1")
scaler = ScalerCH("prj:scaler1", name="scaler")
scaler.preset_time.put(0.4)
scaler.match_names()
use_EPICS_scaler_channels(scaler)
print(scaler.read())

RE(bp.count([scaler], num=5), LiveTable([scaler]))
RE(bp.scan([scaler], m1, 1, 5, 5), LiveTable([m1, scaler]))

RE(bp.count([scaler], num=5), LivePlot("scint"))
RE(bp.scan([scaler], m1, 1, 5, 5), LivePlot("scint", "m1"))

RE(bp.count([scaler], num=5), BestEffortCallback())
RE(bp.scan([scaler], m1, 1, 5, 5), BestEffortCallback())

RE.subscribe(BestEffortCallback())

RE(bp.count([scaler], num=5))
RE(bp.scan([scaler], m1, 1, 5, 5))
