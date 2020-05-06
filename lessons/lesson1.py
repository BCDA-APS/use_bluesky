#!/usr/bin/env python

"lesson 1: scaler and count"

from ophyd.scaler import ScalerCH
from bluesky import RunEngine
import bluesky.plans as bp
from apstools.devices import use_EPICS_scaler_channels


def myCallback(key, doc):
    print(key, len(doc))
    for k, v in doc.items():
        print("\t", k, v)
    print("~~~~~~~~~~~~~~~~~")


RE = RunEngine({})

scaler = ScalerCH("sky:scaler1", name="scaler")
scaler.wait_for_connection()
scaler.preset_time.put(1.5)
print(scaler.preset_time.get())

scaler.channels.chan04.chname.put("scint")
scaler.channels.chan07.chname.put("roi1")

scaler.match_names()
use_EPICS_scaler_channels(scaler)
print(scaler.read())
print(RE(bp.count([scaler], num=3), myCallback))
