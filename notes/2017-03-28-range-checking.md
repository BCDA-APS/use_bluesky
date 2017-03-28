# Are certain checks conducted before a scan?

* Q: [limits check before a basic move](#limits-check-before-a-basic-move)
* Q: [limits check before a scan](#limits-check-before-a-scan)
* Q: [What if motor is moving at start of scan?](#what-if-motor-is-moving-at-start-of-scan)

## limits check before a basic move

*A*: out-of-bounds limit caught by ophyd, raised `LimitError: Value 200 outside of range: [-100.0, 100.0]`

    In [1]: wh_pos()

    +------------+----------+------------+------------+
    | Positioner |    Value |  Low Limit | High Limit |
    +------------+----------+------------+------------+
    | m1	 |  0.00000 | -100.00000 |  100.00000 |
    | m2	 |  0.00000 | -100.00000 |  100.00000 |
    | m3	 |  0.00000 | -100.00000 |  100.00000 |
    | m4	 |  0.00000 | -100.00000 |  100.00000 |
    | m5	 |  0.00000 | -100.00000 |  100.00000 |
    | m6	 |  0.00000 | -100.00000 |  100.00000 |
    | m7	 |  0.00000 | -100.00000 |  100.00000 |
    | m8	 |  0.00000 | -100.00000 |  100.00000 |
    +------------+----------+------------+------------+

    In [2]: mv(m3, 200)
    /bin/bash: -c: line 0: syntax error near unexpected token `m3,'
    /bin/bash: -c: line 0: `mv (m3, 200)'

    In [3]: m3.move(200)
    ---------------------------------------------------------------------------
    LimitError  			      Traceback (most recent call last)
    <ipython-input-3-c4455fa000c6> in <module>()
    ----> 1 m3.move(200)

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/ophyd/utils/epics_pvs.py in wrapper(self, *args, **kwargs)
    	354	def wrapper(self, *args, **kwargs):
    	355	    if self.connected:
    --> 356		return fcn(self, *args, **kwargs)
    	357	    else:
    	358		raise DisconnectedError('{} is not connected'.format(self.name))

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/ophyd/epics_motor.py in move(self, position, wait, **kwargs)
    	153	    self._started_moving = False
    	154
    --> 155	    status = super().move(position, **kwargs)
    	156	    self.user_setpoint.put(position, wait=False)
    	157

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/ophyd/positioner.py in move(self, position, moved_cb, timeout)
    	113		timeout = self._timeout
    	114
    --> 115	    self.check_value(position)
    	116
    	117	    self._run_subs(sub_type=self._SUB_REQ_DONE, success=False)

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/ophyd/epics_motor.py in check_value(self, pos)
    	221	def check_value(self, pos):
    	222	    '''Check that the position is within the soft limits'''
    --> 223	    self.user_setpoint.check_value(pos)
    	224
    	225	def _pos_changed(self, timestamp=None, value=None, **kwargs):

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/ophyd/signal.py in check_value(self, value)
    	820	    if not (low_limit <= value <= high_limit):
    	821		raise LimitError('Value {} outside of range: [{}, {}]'
    --> 822				 .format(value, low_limit, high_limit))
    	823
    	824	@raise_if_disconnected

    LimitError: Value 200 outside of range: [-100.0, 100.0]

## limits check before a scan

*A*: This was not caught until the specific move that would violate the limits was caught by ophyd.
Again, this returned `LimitError: Value 5.125 outside of range: [-5.0, 5.0]` but only after the first
three points of the scan had been collected.

    In [15]: wh_pos()

    +------------+----------+------------+------------+
    | Positioner |    Value |  Low Limit | High Limit |
    +------------+----------+------------+------------+
    | m1	 |  0.00000 | -100.00000 |  100.00000 |
    | m2	 |  0.00000 | -100.00000 |  100.00000 |
    | m3	 |  4.75000 |	-5.00000 |    5.00000 |
    | m4	 |  0.00000 | -100.00000 |  100.00000 |
    | m5	 |  0.00000 | -100.00000 |  100.00000 |
    | m6	 |  0.00000 | -100.00000 |  100.00000 |
    | m7	 |  0.00000 | -100.00000 |  100.00000 |
    | m8	 |  0.00000 | -100.00000 |  100.00000 |
    +------------+----------+------------+------------+

    In [16]: RE(scan([noisy], m3, 4, 5.5, 5), LiveTable([noisy, m3]), comment='limits')
    Transient Scan ID: 10
    Persistent Unique Scan ID: 'b61b85fb-aefe-4e92-b9e4-9cd5128ce2a8'
    +-----------+------------+------------+------------+------------------+
    |	seq_num |	time |      noisy |	    m3 | m3_user_setpoint |
    +-----------+------------+------------+------------+------------------+
    |	      1 | 15:49:32.9 |    9.98616 |    4.00000 |	  4.00000 |
    |	      2 | 15:49:33.4 |    9.98786 |    4.38000 |	  4.37500 |
    |	      3 | 15:49:34.0 |    9.99942 |    4.75000 |	  4.75000 |
    +-----------+------------+------------+------------+------------------+
    generator scan ['b61b85'] (scan num: 10)
    ['descriptors', 'start', 'stop']
    wrote: /home/oxygen18/JEMIAN/Documents/gov_10.h5
    ---------------------------------------------------------------------------
    LimitError  			      Traceback (most recent call last)
    <ipython-input-16-4f4f3cb302b3> in <module>()
    ----> 1 RE(scan([noisy], m3, 4, 5.5, 5), LiveTable([noisy, m3]), comment='limits')

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/bluesky/run_engine.py in __call__(self, plan, subs, raise_if_interrupted, **metadata_kw)
    	597			# it (unless it is a canceled error)
    	598			if exc is not None:
    --> 599			    raise exc
    	600
    	601		if raise_if_interrupted and self._interrupted:

    /APSshare/anaconda3/BlueSky/lib/python3.5/asyncio/tasks.py in _step(***failed resolving arguments***)
    	237		    # We use the `send` method directly, because coroutines
    	238		    # don't have `__iter__` and `__next__` methods.
    --> 239		    result = coro.send(None)
    	240		else:
    	241		    result = coro.throw(exc)

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/bluesky/run_engine.py in _run(self)
       1005		self.log.error("Run aborted")
       1006		self.log.error("%r", err)
    -> 1007		raise err
       1008	    finally:
       1009		# Some done_callbacks may still be alive in other threads.

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/bluesky/run_engine.py in _run(self)
    	903			    resp = self._response_stack.pop()
    	904			    try:
    --> 905				msg = self._plan_stack[-1].send(resp)
    	906			    # We have exhausted the top generator
    	907			    except StopIteration:

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/bluesky/plans.py in scan(detectors, motor, start, stop, num, per_step, md)
       2143		yield from per_step(detectors, motor, step)
       2144
    -> 2145	return (yield from inner_scan())
       2146
       2147

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/bluesky/plans.py in dec_inner(*inner_args, **inner_kwargs)
    	 45		    plan = gen_func(*inner_args, **inner_kwargs)
    	 46		    plan = wrapper(plan, *args, **kwargs)
    ---> 47		    return (yield from plan)
    	 48		return dec_inner
    	 49	    return dec

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/bluesky/plans.py in stage_wrapper(plan, devices)
       1508	    return (yield from plan)
       1509
    -> 1510	return (yield from finalize_wrapper(inner(), unstage_devices()))
       1511
       1512

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/bluesky/plans.py in finalize_wrapper(plan, final_plan, pause_for_debug)
       1023	cleanup = True
       1024	try:
    -> 1025	    ret = yield from plan
       1026	except GeneratorExit:
       1027	    cleanup = False

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/bluesky/plans.py in inner()
       1506	def inner():
       1507	    yield from stage_devices()
    -> 1508	    return (yield from plan)
       1509
       1510	return (yield from finalize_wrapper(inner(), unstage_devices()))

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/bluesky/plans.py in dec_inner(*inner_args, **inner_kwargs)
    	 45		    plan = gen_func(*inner_args, **inner_kwargs)
    	 46		    plan = wrapper(plan, *args, **kwargs)
    ---> 47		    return (yield from plan)
    	 48		return dec_inner
    	 49	    return dec

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/bluesky/plans.py in run_wrapper(plan, md)
    	871	"""
    	872	yield from open_run(md)
    --> 873	yield from plan
    	874	rs_uid = yield from close_run()
    	875	return rs_uid

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/bluesky/plans.py in inner_scan()
       2141	def inner_scan():
       2142	    for step in steps:
    -> 2143		yield from per_step(detectors, motor, step)
       2144
       2145	return (yield from inner_scan())

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/bluesky/plans.py in one_1d_step(detectors, motor, step)
       2007	    yield Msg('wait', None, group=grp)
       2008
    -> 2009	yield from move()
       2010	return (yield from trigger_and_read(list(detectors) + [motor]))
       2011

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/bluesky/plans.py in move()
       2004	    grp = _short_uid('set')
       2005	    yield Msg('checkpoint')
    -> 2006	    yield Msg('set', motor, step, group=grp)
       2007	    yield Msg('wait', None, group=grp)
       2008

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/bluesky/run_engine.py in _run(self)
    	954			    # exceptions (coming in via throw) can be
    	955			    # raised
    --> 956			    response = yield from coro(msg)
    	957			# special case `CancelledError` and let the outer
    	958			# exception block deal with it.

    /APSshare/anaconda3/BlueSky/lib/python3.5/asyncio/coroutines.py in coro(*args, **kw)
    	204	    @functools.wraps(func)
    	205	    def coro(*args, **kw):
    --> 206		res = func(*args, **kw)
    	207		if isinstance(res, futures.Future) or inspect.isgenerator(res) or \
    	208			isinstance(res, CoroWrapper):

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/bluesky/run_engine.py in _set(self, msg)
       1646	    group = kwargs.pop('group', None)
       1647	    self._movable_objs_touched.add(msg.obj)
    -> 1648	    ret = msg.obj.set(*msg.args, **kwargs)
       1649	    p_event = asyncio.Event(loop=self.loop)
       1650	    pardon_failures = self._pardon_failures

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/ophyd/positioner.py in set(self, new_position, wait, moved_cb, timeout)
    	194	    """
    	195	    return self.move(new_position, wait=wait, moved_cb=moved_cb,
    --> 196			     timeout=timeout)
    	197
    	198	def _repr_info(self):

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/ophyd/utils/epics_pvs.py in wrapper(self, *args, **kwargs)
    	354	def wrapper(self, *args, **kwargs):
    	355	    if self.connected:
    --> 356		return fcn(self, *args, **kwargs)
    	357	    else:
    	358		raise DisconnectedError('{} is not connected'.format(self.name))

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/ophyd/epics_motor.py in move(self, position, wait, **kwargs)
    	153	    self._started_moving = False
    	154
    --> 155	    status = super().move(position, **kwargs)
    	156	    self.user_setpoint.put(position, wait=False)
    	157

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/ophyd/positioner.py in move(self, position, moved_cb, timeout)
    	113		timeout = self._timeout
    	114
    --> 115	    self.check_value(position)
    	116
    	117	    self._run_subs(sub_type=self._SUB_REQ_DONE, success=False)

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/ophyd/epics_motor.py in check_value(self, pos)
    	221	def check_value(self, pos):
    	222	    '''Check that the position is within the soft limits'''
    --> 223	    self.user_setpoint.check_value(pos)
    	224
    	225	def _pos_changed(self, timestamp=None, value=None, **kwargs):

    /APSshare/anaconda3/BlueSky/lib/python3.5/site-packages/ophyd/signal.py in check_value(self, value)
    	820	    if not (low_limit <= value <= high_limit):
    	821		raise LimitError('Value {} outside of range: [{}, {}]'
    --> 822				 .format(value, low_limit, high_limit))
    	823
    	824	@raise_if_disconnected

    LimitError: Value 5.125 outside of range: [-5.0, 5.0]

## What if motor is moving at start of scan?

*A*: Apparently, there is no check at the start of a scan that waits because a motor is moving.

    In [43]: print(m3.position)
    	...: m3.move(-4, wait=False)   # PyEpics:  epics.caput(m3.prefix, -4)
    	...: sleep(0.5)
    	...: print(m3.position)
    	...: RE(scan([noisy], m3, 4, 4.5, 5), LiveTable([noisy, m3]), comment='was moving, OK?')
    	...:
    4.5
    4.11
    Transient Scan ID: 14
    Persistent Unique Scan ID: 'a823c794-3d0d-40e5-abe6-0762d92f76c5'
    +-----------+------------+------------+------------+------------------+
    |	seq_num |	time |      noisy |	    m3 | m3_user_setpoint |
    +-----------+------------+------------+------------+------------------+
    |	      1 | 16:07:34.8 |    9.99924 |    4.00000 |	  4.00000 |
    |	      2 | 16:07:35.2 |    9.99668 |    4.13000 |	  4.12500 |
    |	      3 | 16:07:35.6 |    9.99079 |    4.25000 |	  4.25000 |
    |	      4 | 16:07:36.0 |    9.99181 |    4.38000 |	  4.37500 |
    |	      5 | 16:07:36.4 |    9.99791 |    4.50000 |	  4.50000 |
    +-----------+------------+------------+------------+------------------+
    generator scan ['a823c7'] (scan num: 14)
    ['descriptors', 'start', 'stop']
    wrote: /home/oxygen18/JEMIAN/Documents/gov_14.h5
    Value 5.125 outside of range: [-5.0, 5.0]
    Out[43]: ['a823c794-3d0d-40e5-abe6-0762d92f76c5']

