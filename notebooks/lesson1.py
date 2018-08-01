#!/APSshare/anaconda3/BlueSky/bin/python

"lesson 1: scaler"

from ophyd.scaler import ScalerCH
from bluesky import RunEngine
import bluesky.plans as bp
from APS_BlueSky_tools.devices import use_EPICS_scaler_channels


def myCallback(key, doc):
    print(key, len(doc))
    for k, v in doc.items():
        print("\t", k, v)
    print("~~~~~~~~~~~~~~~~~")


RE = RunEngine({})

scaler = ScalerCH("prj:scaler1", name="scaler")
scaler.preset_time.put(1.5)
print(scaler.preset_time.value)

scaler.channels.chan04.chname.put("scint")
scaler.channels.chan07.chname.put("roi1")

scaler.match_names()
use_EPICS_scaler_channels(scaler)
print(scaler.read())
print(RE(bp.count([scaler], num=3), myCallback))
