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


import inspect
import numpy as np
#from bluesky.global_state import gs
from bluesky import plans
from bluesky.callbacks.core import CallbackBase 
import epics


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
    :func:`bluesky.plans.relative_scan`
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
        self.scan_id = doc["scan_id"] 
        self.num_projections = doc["num_projections"]
        self.scan_label = "%s %d (%s)" % (self.plan_name, self.scan_id, self.short_uid)
        msg = "start: " + self.scan_label
        self.plan_name + ': ' + self.short_uid
        epics.caput(self.msg_pv_a, msg)
        epics.caput(self.msg_pv_b, "")
    
    def event(self, doc):
        msg = "event %d of %d" % (doc["seq_num"], self.num_projections)
        progress = 100.0 * doc["seq_num"] / self.num_projections
        msg += " (%.0f%%)" % progress
        epics.caput(self.msg_pv_b, msg)
    
    def stop(self, doc):
        msg = "End: " + self.scan_label
        epics.caput(self.msg_pv_a, msg)
        epics.caput(self.msg_pv_b, "")

# def interlace_tomo_per_step(detectors, motor, step):
#     """
#     per_step: to customize the handling of each projection in a scan
#     """
#     # def move():
#     #     grp = _short_uid('set')
#     #     yield Msg('checkpoint')
#     #     yield Msg('set', motor, step, group=grp)
#     #     yield Msg('wait', None, group=grp)
#     # 
#     # yield from move()
#     # return (yield from trigger_and_read(list(detectors) + [motor]))
