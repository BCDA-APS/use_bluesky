print(__file__)
from ophyd import (PVPositioner, EpicsMotor, EpicsSignal, EpicsSignalRO,
                   PVPositionerPC, Device)
from ophyd import Component as Cpt

class MotorDialValues(Device):
	value = Cpt(EpicsSignalRO, ".DRBV")
	setpoint = Cpt(EpicsSignal, ".DVAL")

class MyEpicsMotorWithDial(EpicsMotor):
	dial = Cpt(MotorDialValues, "")

# m1 = MyEpicsMotorWithDial('xxx:m1', name='m1')

m1 = EpicsMotor('xxx:m1', name='m1')
m2 = EpicsMotor('xxx:m2', name='m2')
m3 = EpicsMotor('xxx:m3', name='m3')
m4 = EpicsMotor('xxx:m4', name='m4')
m5 = EpicsMotor('xxx:m5', name='m5')
m6 = EpicsMotor('xxx:m6', name='m6')
m7 = EpicsMotor('xxx:m7', name='m7')
m8 = EpicsMotor('xxx:m8', name='m8')
