#!/APSshare/anaconda3/BlueSky/bin/python

"lesson 3: Show the data as it is acquired"

from ophyd import EpicsMotor
from ophyd.scaler import ScalerCH
from bluesky import RunEngine
import bluesky.plans as bp
from bluesky.callbacks import LiveTable
from bluesky.callbacks import LivePlot
from bluesky.callbacks.best_effort import BestEffortCallback
from apstools.devices import use_EPICS_scaler_channels


%matplotlib notebook
from bluesky.utils import install_qt_kicker
install_qt_kicker()


RE = RunEngine({})

P = "vm7:"
m1 = EpicsMotor(f"{P}m1", name="m1")
scaler = ScalerCH(f"{P}scaler1", name="scaler")
scaler.preset_time.put(0.4)
scaler.select_channels(None)
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
