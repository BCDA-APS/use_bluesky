logger.info(__file__)

"""signals"""

# APS only:
# aps = APS_devices.ApsMachineParametersDevice(name="aps")
# sd.baseline.append(aps)

# undulator = APS_devices.ApsUndulatorDual("ID45", name="undulator")
# sd.baseline.append(undulator)


# simulate a shutter (no hardware required)
shutter = SimulatedApsPssShutterWithStatus(name="shutter")
shutter.delay_s = 0.05 # shutter needs short recovery time after moving
