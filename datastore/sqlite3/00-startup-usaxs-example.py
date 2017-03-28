import ophyd
from ophyd import setup_ophyd
import databroker
setup_ophyd()
import portable_mds.sqlite.mds as pmqsm
from ophyd import EpicsSignal, Device, EpicsMotor, Component as Cpt
from bluesky.utils import install_qt_kicker
install_qt_kicker()

import matplotlib.pyplot as plt
plt.ion()


class UsaxsXyStage(Device):
    x = Cpt(EpicsMotor, 'm1')
    y = Cpt(EpicsMotor, 'm2')

sample_stage = UsaxsXyStage('9idcLAX:m58:c2:', name='sample_stage')


mds_config = {
    'directory': '/share1/bluesky/mds',    # for *.sqlite file each scan
    'timezone': 'US/Central'
}
mds = pmqsm.MDS(config=mds_config)


import bluesky as bs
import bluesky.plans as bp
from bluesky.callbacks import LiveTable, LivePlot

RE = bs.RunEngine({})
RE.subscribe('all', mds.insert)

db = databroker.Broker(mds, None)
