
"""
lesson 5 : get motor and scaler from ophyd simulators
"""

__all__ = [
    'motor',
    'noisy', 
    ]

from ...session_logs import logger
logger.info(__file__)

import numpy as np
from ophyd.sim import motor, SynGauss


noisy = SynGauss(
    'noisy', 
    motor, 'motor', 
    # center somewhere between -1 and 1
    center=2 * (np.random.random()-0.5), 
    # randomize these parameters
    Imax=100000 + 20000 * (np.random.random()-0.5),
    noise='poisson', 
    sigma=0.016 + 0.015 * (np.random.random()-0.5), 
    noise_multiplier=0.1 + 0.02 * (np.random.random()-0.5),
    labels={'detectors'})


motor.precision = 5
noisy.precision = 0