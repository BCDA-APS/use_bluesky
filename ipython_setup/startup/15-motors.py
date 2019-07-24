logger.info(__file__)

"""the motors"""

try:
    m1 = EpicsMotor('xxx:m1', name='m1', labels=("motor", "general"))
    m2 = EpicsMotor('xxx:m2', name='m2', labels=("motor", "general"))
    m3 = EpicsMotor('xxx:m3', name='m3', labels=("motor", "general"))
    m4 = EpicsMotor('xxx:m4', name='m4', labels=("motor", "general"))
    m5 = EpicsMotor('xxx:m5', name='m5', labels=("motor", "demo"))
    m6 = EpicsMotor('xxx:m6', name='m6', labels=("motor", "demo"))
    m7 = EpicsMotor('xxx:m7', name='m7', labels=("motor", "demo"))
    m8 = EpicsMotor('xxx:m8', name='m8', labels=("motor", "demo"))
except TimeoutError:
    logger.warning(f"Could not connect 15-motors.py")
