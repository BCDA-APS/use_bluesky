#!/usr/bin/env python

"""
demonstrate an interlace tomography scan plan in BlueSky

:see: https://github.com/BCDA-APS/use_bluesky/issues/4

INITIAL ALGORITHM : interlaced tomo scan

At each step of the resultant scan, a projection image is recorded.

An outer loop steps over a list of starting points and
executes a series of steps (by the inner loop).  Together,
the two loops, using the same movable, map out a fine
density of positions across the scanned space of the movable.

The full range of the outer loop should be less than the
step size of the inner loop to map out the movable.

* inner loop: rotation steps from a given start
* outer loop: set of starting points for inner loop

NOTES

* prior: https://github.com/dgursoy/mona/blob/master/trunk/32id/tomo_step_scan.py
* that code provided `tomo_scan()`
* took its parameters from a global dictionary: `variableDict`, 
  relevant keys::

    'Projections': 361,
    'SampleStart_Rot': 0.0,
    'SampleEnd_Rot': 180.0,
    'ExposureTime': 3,

"""


import os
import inspect
import numpy as np
import numpy.ma as ma
#from bluesky.global_state import gs
from bluesky import plans
from bluesky.callbacks.core import CallbackBase 
import epics
from ophyd.epics_motor import EpicsMotor
from ophyd import AreaDetector
import time

def tomo_scan(detectors, motor, start, stop, num, *, per_step=None, md={}):
    """
    tomography scan plan (based on `plans.scan()`)
    
    :see: https://github.com/dgursoy/mona/blob/master/trunk/32id/tomo_step_scan.py
    :seealso: http://nsls-ii.github.io/bluesky/bluesky.plans.scan.html#bluesky.plans.scan
    :seealso: https://github.com/NSLS-II/bluesky/blob/master/bluesky/plans.py#L2032

    Parameters
    ----------
    
    :param [readable] detectors: list of 'readable' objects
    :param obj motor: instance of `setable` (motor, temp controller, etc.)
    :param float start: first position of `motor`
    :param float stop: last position of `motor`
    :param int num: number of projections
    :param obj per_step: (optional) a `callable`

        * custom override of standard inner loop handling (at each point of the scan)
        * Expected signature: ``f(detectors, motor, step)``
    
    :param dict md: (optional) metadata dictionary

    See Also
    --------
    :func:`bluesky.plans.scan`
    """
    _md = {'detectors': [det.name for det in detectors],
          'motors': [motor.name],
          'num_projections': num,
          'plan_args': {'detectors': list(map(repr, detectors)), 'num': num,
                        'motor': repr(motor),
                        'start': start, 'stop': stop,
                        'per_step': repr(per_step)},
          'plan_name': inspect.currentframe().f_code.co_name,
          'plan_pattern': 'linspace',
          'plan_pattern_module': 'numpy',
          'plan_pattern_args': dict(start=start, stop=stop, num=num),
         }
    _md.update(md)

    per_step = per_step or plans.one_1d_step

    projections = np.linspace(**_md['plan_pattern_args'])

    @plans.stage_decorator(list(detectors) + [motor])
    @plans.run_decorator(md=_md)
    def inner_scan():
        for projection in projections:
            yield from per_step(detectors, motor, projection)

    return (yield from inner_scan())


def interlace_tomo_scan(detectors, motor, start, stop, inner_num, outer_num, *, per_step=None, md={}, snake=False):
    """
    interlace tomography scan plan (based on `plans.scan()`)
    
    :see: https://github.com/dgursoy/mona/blob/master/trunk/32id/tomo_step_scan.py
    :seealso: http://nsls-ii.github.io/bluesky/bluesky.plans.scan.html#bluesky.plans.scan
    :seealso: https://github.com/NSLS-II/bluesky/blob/master/bluesky/plans.py#L2032

    Parameters
    ----------
    
    :param [readable] detectors: list of 'readable' objects
    :param obj motor: instance of `setable` (motor, temp controller, etc.)
    :param float start: first position of `motor`
    :param float stop: last position of `motor`
    :param int inner_num: number of projections in the inner loop
    :param int outer_num: number of projections in the outer loop
    :param obj per_step: (optional) a `callable`

        * custom override of standard inner loop handling (at each point of the scan)
        * Expected signature: ``f(detectors, motor, step)``
    
    :param dict md: (optional) metadata dictionary
    :param bool snake: (optional) move inner loop back and forth or always in given direction (default: False)

    See Also
    --------
    :func:`bluesky.plans.scan`
    """
    # work out the sequence of projections in advance, normal 1-D scan handling after that
    inner = np.linspace(start, stop, inner_num)
    outer = np.linspace(0, inner[1]-inner[0], 1+outer_num)
    projections = inner
    for i, offset in enumerate(outer[1:-1]):
        if snake and i%2 == 0:
            # http://stackoverflow.com/questions/6771428/most-efficient-way-to-reverse-a-numpy-array#6771620
            projections = np.append(projections, offset + inner[::-1])
        else:
            projections = np.append(projections, offset + inner)
    # only keep the points within the range: start ...stop
    projections = ma.compressed(ma.masked_outside(projections, start, stop))
    
    num = len(projections)

    _md = {'detectors': [det.name for det in detectors],
          'motors': [motor.name],
          'num_projections': num,
          'plan_args': {'detectors': list(map(repr, detectors)), 'num': num,
                        'motor': repr(motor),
                        'start': start, 'stop': stop,
                        'per_step': repr(per_step)},
          'plan_name': inspect.currentframe().f_code.co_name,
          'plan_pattern': 'linspace',
          'plan_pattern_module': 'numpy',
          'plan_pattern_args': dict(start=start, 
                                    stop=stop, 
                                    inner_num=inner_num, 
                                    outer_num=outer_num, 
                                    snake=snake),
         }
    _md.update(md)

    per_step = per_step or plans.one_1d_step

    @plans.stage_decorator(list(detectors) + [motor])
    @plans.run_decorator(md=_md)
    def inner_scan():
        for projection in projections:
            yield from per_step(detectors, motor, projection)

    return (yield from inner_scan())


class FrameNotifier(CallbackBase):

    def __init__(self, areadet, *args, path=None, **kws):
        # TODO: assert areadet is a subclass of AreaDetector
        self.areadet = areadet
        self.path = path or os.getcwd()
        if not os.path.exists(self.path):
            msg = 'path: ' + self.path + ' does not exist'
            raise ValueError(msg)

    def start(self, doc):
        hdf5_prefix = self.areadet.name + 'HDF1:'
        short_uid = doc["uid"].split("-")[0]
        epics.caput(hdf5_prefix + 'EnableCallbacks', 'Enable')
        epics.caput(hdf5_prefix + 'ArrayCallbacks', 'Enable')
        epics.caput(hdf5_prefix + 'FilePath', self.path)
        epics.caput(hdf5_prefix + 'FileName', 'ts_' + short_uid)
        epics.caput(hdf5_prefix + 'FileNumber', 0)  # or 1?
        epics.caput(hdf5_prefix + 'AutoIncrement', 'Yes')
        epics.caput(hdf5_prefix + 'FileTemplate', '%s%s_%5.5d.h5')
        epics.caput(hdf5_prefix + 'AutoSave', 'Yes')
        epics.caput(hdf5_prefix + 'FileWriteMode', 'Single')


class EPICSNotifierCallback(CallbackBase):
    """
    callback handler: update a couple EPICS string PVs
    """
    
    def __init__(self, msg_pv_a, msg_pv_b, *args, **kws):
        self.msg_pv_a = msg_pv_a
        self.msg_pv_b = msg_pv_b
        self.num_projections = None
        self.plan_name = None
        self.short_uid = None
        self.scan_id = None
        self.scan_label = None
        epics.caput(self.msg_pv_a, "")
        epics.caput(self.msg_pv_b, "")
    
    def start(self, doc):
        self.plan_name = doc["plan_name"]
        self.short_uid = doc["uid"].split("-")[0]
        # TODO: setup area detector (if using) HDF5 plugin
        #   FilePath = ???    # let user decide or os.getcwd()
        #   FileName = self.short_uid
        #   FileNumber = 0    # or 1?
        self.scan_id = doc["scan_id"] 
        self.num_projections = doc["num_projections"]
        self.scan_label = "%s %d (%s)" % (self.plan_name, self.scan_id, self.short_uid)
        msg = "start: " + self.scan_label
        self.plan_name + ': ' + self.short_uid
        epics.caput(self.msg_pv_a, msg[:39])
        epics.caput(self.msg_pv_b, "")
    
    def event(self, doc):
        # TODO: document frame file name (if using area detector)
        msg = "event %d of %d" % (doc["seq_num"], self.num_projections)
        progress = 100.0 * doc["seq_num"] / self.num_projections
        msg += " (%.1f%%)" % progress
        epics.caput(self.msg_pv_b, msg[:39])
    
    def stop(self, doc):
        msg = "End: " + self.scan_label
        epics.caput(self.msg_pv_a, msg[:39])
        epics.caput(self.msg_pv_b, "")


class PreTomoScanChecks(CallbackBase):
    """
    callback handler: update a couple EPICS string PVs
    
    ATTRIBUTES
    
    :param readable source_intensity: signal that describes source intensity now

    ATTRIBUTES
    
    :param float source_intensity_threshold:
        minimum acceptable source intensity
        (default: 1.0 in units of `source_intensity`)
    :param int report_interval:
        when waiting for beam, make UI reports on this interval
        (default: 60, units: seconds)
    :param int recheck_interval:
        when waiting for beam, re-check on this interval
        (default: 1, units: seconds)
    """
    
    def __init__(self, motor, source_intensity=None):
        self.motor = motor
        self.source_intensity = source_intensity
        self.source_intensity_threshold = 1.0   # arbitrary default
        self.report_interval = 60
        self.recheck_interval = 1
    
    def start(self, doc):
        self.check_beam()
        
        self.check_motor_moving(self.motor)
        
        args = doc["plan_args"]
        for key in "start stop".split():
            self.check_motor_limits(self.motor, args[key])
    
    def check_beam(self):
        if self.source_intensity is not None:
            t_ref = time.time.now()
            t_update = t_ref + 1    # first report comes early
            while self.source_intensity < self.source_intensity_threshold:
                t = time.time.now()
                if t >= t_update:
                    t_update += t + self.report_interval
                    h = int((t - t_ref + 0.5) / 3600)
                    m = int(((t - t_ref + 0.5) % 3600) / 60)
                    s = int((t - t_ref + 0.5) % 60)
                    msg = 'waiting for beam:'
                    if h > 0:
                        msg += ' %dh' % h
                    if h > 0:
                        msg += ' %dm' % m
                    msg += ' %ds' % s
                    print(msg)

    
    def check_motor_moving(self, motor):
        # TODO: this assume a PyEpics motor object, generalize this check
        assert(isinstance(motor, EpicsMotor))
        if not motor.motor_done_move:
            msg = "motor " + motor.name + " is moving, scan canceled"
            raise ValueError(msg)
    
    def check_motor_limits(self, motor, target):
        # TODO: there is an ophyd method for this test
        # TODO: this assume a PyEpics motor object, generalize this check
        # ? backlash distance ?
        assert(isinstance(motor, EpicsMotor))
        if not motor.low_limit <= target <= motor.high_limit:
            msg = str(target)
            msg += " is outside of limits ("
            msg += str(motor.low_limit)
            msg += ", "
            msg += str(motor.high_limit)
            msg += ") for motor " + motor.name
            msg += ", scan canceled"
            raise ValueError(msg)
