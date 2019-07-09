print(__file__)

"""detectors (area detectors handled separately)"""

scaler = ScalerCH('xxx:scaler1', name='scaler')
while not scaler.connected:
	time.sleep(0.1)
scaler.select_channels(None)

# demo: use this swait record to make a "noisy" detector signal
noisy = EpicsSignalRO('xxx:userCalc1', name='noisy')
