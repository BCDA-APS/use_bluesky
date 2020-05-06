
"""
APS only: connect with facility information
"""

__all__ = [
    'aps', 
    # 'undulator',
    ]

from ..session_logs import logger
logger.info(__file__)

from ophyd import EpicsMotor, EpicsSignal
from ophyd.scaler import ScalerCH

tth = EpicsMotor('29idKappa:m9', name='tth', labels=('motor',))  # Two Theta
# 1: MOT001 =    NONE   2000  1  2000  200   50  125    0 0x003       th  Theta  # Theta
# 2: MOT002 =    NONE   2000  1  2000  200   50  125    0 0x003      chi  Chi  # Chi
# 3: MOT003 =    NONE   2000  1  2000  200   50  125    0 0x003      phi  Phi  # Phi
kth = EpicsMotor('29idKappa:m8', name='kth', labels=('motor',))  # K_Theta
kap = EpicsMotor('29idKappa:m7', name='kap', labels=('motor',))  # Kappa
kphi = EpicsMotor('29idKappa:m1', name='kphi', labels=('motor',))  # K_Phi
s1at = EpicsMotor('29idb:m9', name='s1at', labels=('motor',))  # Sl1A top
s1ai = EpicsMotor('29idb:m10', name='s1ai', labels=('motor',))  # Sl1A inb
s1ao = EpicsMotor('29idb:m11', name='s1ao', labels=('motor',))  # Sl1A out
s1ab = EpicsMotor('29idb:m12', name='s1ab', labels=('motor',))  # Sl1A bot
s2ai = EpicsMotor('29idb:m13', name='s2ai', labels=('motor',))  # Sl2A inb
s2ao = EpicsMotor('29idb:m14', name='s2ao', labels=('motor',))  # Sl2A out
s2ab = EpicsMotor('29idb:m15', name='s2ab', labels=('motor',))  # Sl2A bot
s2at = EpicsMotor('29idb:m16', name='s2at', labels=('motor',))  # Sl2A top
slit3b = EpicsMotor('29idb:m26', name='slit3b', labels=('motor',))  # Sl3D bottom
slit3t = EpicsMotor('29idb:m27', name='slit3t', labels=('motor',))  # Sl3D top
d4d = EpicsMotor('29idb:m25', name='d4d', labels=('motor',))  # D4-D
d5d = EpicsMotor('29idb:m28', name='d5d', labels=('motor',))  # D5-D
mmesh = EpicsMotor('29idb:m5', name='mmesh', labels=('motor',))  # mesh
vdiag = EpicsMotor('29idb:m4', name='vdiag', labels=('motor',))  # Vdiag
samx = EpicsMotor('29idKappa:m2', name='samx', labels=('motor',))  # SampleX
samy = EpicsMotor('29idKappa:m3', name='samy', labels=('motor',))  # SampleY
samz = EpicsMotor('29idKappa:m4', name='samz', labels=('motor',))  # SampleZ
# Macro Motor: SpecMotor(mne='iexmono', config_line='24', name='IEXmono', macro_prefix='Mono')  # IEXmono # read_mode=7

scaler1 = ScalerCH('29idMZ0:scaler1', name='scaler1', labels=('detectors',))
# counter: sec = SpecCounter(mne='sec', config_line='0', name='Seconds', unit='0', chan='0', pvname=29idMZ0:scaler1.S1)
mon = EpicsSignal('29idMZ0:scaler1.S14', name='mon', labels=('detectors',))  # Monitor
srs2 = EpicsSignal('29idMZ0:scaler1.S2', name='srs2', labels=('detectors',))  # SRS2
srs3 = EpicsSignal('29idMZ0:scaler1.S3', name='srs3', labels=('detectors',))  # SRS3
srs4 = EpicsSignal('29idMZ0:scaler1.S4', name='srs4', labels=('detectors',))  # SRS4
mcp = EpicsSignal('29idMZ0:scaler1.S5', name='mcp', labels=('detectors',))  # MCP
samT = EpicsSignal('29idd:LS331:TC1:SampleA', name='samT', labels=('detectors',))  # TA
cryoT = EpicsSignal('29idd:LS331:TC1:SampleB', name='cryoT', labels=('detectors',))  # TB
tey = EpicsSignal('29idd:ca2:read', name='tey', labels=('detectors',))  # CA2
ca3 = EpicsSignal('29idd:ca3:read', name='ca3', labels=('detectors',))  # CA3
ca4 = EpicsSignal('29idd:ca4:read', name='ca4', labels=('detectors',))  # CA4
id_rbv = EpicsSignal('ID29:EnergyRBV', name='id_rbv', labels=('detectors',))  # ID_RBV
mode = EpicsSignal('ID29:ActualMode', name='mode', labels=('detectors',))  # ID_Mode
sr = EpicsSignal('S:SRcurrentAI', name='sr', labels=('detectors',))  # SR
energy = EpicsSignal('29idmono:ENERGY_SP', name='energy', labels=('detectors',))
setbl = EpicsSignal('29id:BeamlineEnergySet', name='setbl', labels=('detectors',))  # SetBL
th_rbv = EpicsSignal('29idKappa:userCalcOut1.VAL', name='th_rbv', labels=('detectors',))  # THETA
tth_rbv = EpicsSignal('29idKappa:m9.RBV', name='tth_rbv', labels=('detectors',))  # TTH
mpa = EpicsSignal('29idMZ0:scaler1.S14', name='mpa', labels=('detectors',))  # MPA
