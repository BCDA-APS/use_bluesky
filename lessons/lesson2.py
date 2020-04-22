#!/usr/bin/env python

"lesson 2: motor and scan"

from ophyd import EpicsMotor
from ophyd.scaler import ScalerCH
from bluesky import RunEngine
import bluesky.plans as bp
from apstools.devices import use_EPICS_scaler_channels


def myCallback(key, doc):
    print(key, len(doc))
    for k, v in doc.items():
        print("\t", k, v)
    print("~~~~~~~~~~~~~~~~~")


m1 = EpicsMotor("sky:m1", name="m1")
m1.wait_for_connection()

print(m1.position)

scaler = ScalerCH("sky:scaler1", name="scaler")
scaler.wait_for_connection()
scaler.preset_time.put(0.5)


# Since there are no detectors actually connected to this scaler,
# we can change names at our choice.  A real scaler will have
# detectors connected to specific channels and we should not modify
# these names without regard to how signals are physically connected.
scaler.channels.chan01.chname.put("clock")
scaler.channels.chan02.chname.put("I0")
scaler.channels.chan03.chname.put("scint")
scaler.channels.chan04.chname.put("")
scaler.channels.chan05.chname.put("")
scaler.channels.chan06.chname.put("")
scaler.channels.chan07.chname.put("")
scaler.channels.chan08.chname.put("")
scaler.channels.chan09.chname.put("")


scaler.match_names()
use_EPICS_scaler_channels(scaler)
print(scaler.read())

RE = RunEngine({})

RE(bp.scan([scaler], m1, -1, 1, 5))

RE(bp.scan([scaler], m1, -1, 1, 5), myCallback)
