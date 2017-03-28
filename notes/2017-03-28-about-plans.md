# Overview: What is a BlueSky *plan*?

In [BlueSky](https://github.com/NSLS-II/bluesky), all activity happens by the execution of a *plan*.
A BlueSky *plan* is a Python function that calls a sequence of BlueSky *messages* which
constitute data acquisition operations 
such as a scan or even the collection of a single value, such as counting from a scaler.

The BlueSky documentation provides and [introduction](http://nsls-ii.github.io/bluesky/plans_intro.html)
to [plans](http://nsls-ii.github.io/bluesky/plans.html).
This document expands to describe more details about BlueSky *plans*.

**summary**: 

* *plan* : Python command that executes a sequence of *messages*.
* *message* : instance of [`bluesky.utils.Msg`](https://github.com/NSLS-II/bluesky/blob/master/bluesky/utils.py#L23).

    Msg(command, obj, *args, **kwargs)

## The BlueSky *Run Engine*

To understand the BlueSky *plan*, it is first necessary to understand in what context
a plan is used.

The *RunEngine* is a state machine (states: idle, running, paused), 
reponsible for executing a *plan*.  It will emit a stream of BlueSky *documents*
as it executes the plan.  *The Run Engine executes messages and emits Documents.*
(A *document* is the fundamental record of storage in the BlueSky datastore.  It is a 
[json](http://json.org/) string.)

These documents will take one of these forms:

* `start` : first document of a *plan*
* `descriptor`: -TODO- (? description of an event ?)
* `event` : one record of data of a *plan*, includes uid of *start* document
* `stop` : last document of a *plan*, includes uid of *start* document

A plan is *submitted* to the RunEngine through a call such as

    # setup
    from bluesky.global_state import gs
    RE = gs.RE  # convenience alias
    
    #
    RE(a_plan)

note: Specifically, we use `RE` as defined in 
[`bluesky.global_state`](https://github.com/NSLS-II/bluesky/blob/master/bluesky/global_state.py#L121)
as the single instance of the BlueSky *Run Engine*.  In fact, `RE` is an instance
of the `bluesky.global_state.RunEngineTraitType` class.  Use it as a 
[singleton](https://en.wikipedia.org/wiki/Singleton_pattern).

### Examples

Simplest example (from the 
[source code](https://github.com/NSLS-II/bluesky/blob/master/bluesky/run_engine.py#L488)):
    >>> RE(my_scan)

Examples using subscriptions (a.k.a. callbacks):

    >>> def print_data(doc):
    ...     print("Measured: %s" % doc['data'])
    ...
    >>> def celebrate(doc):
    ...     # Do nothing with the input.
    ...     print("The run is finished!!!")
    ...
    >>> RE(my_generator, subs={'event': print_data, 'stop': celebrate})

For every `event` documented emitted by the *Run Engine*, in addition
to anything else done by the *Run Engine*, `print_data()` will be called
and the method will print the contents of the `event` document.

### Definition of the call to `RE()`

[Briefly](https://github.com/NSLS-II/bluesky/blob/master/bluesky/run_engine.py#L488):

    RE(plan, subs=None, *, raise_if_interrupted=False, **metadata_kw)

## *Plan* Examples

see [`bluesky.plans`](https://github.com/NSLS-II/bluesky/blob/master/bluesky/plans.py)

* [`mv`](https://github.com/NSLS-II/bluesky/blob/master/bluesky/plans.py#L439)
* [`count`](https://github.com/NSLS-II/bluesky/blob/master/bluesky/plans.py#L1842)
  : [example](http://nsls-ii.github.io/bluesky/plans.html#time-series-count)
* [`scan`](https://github.com/NSLS-II/bluesky/blob/master/bluesky/plans.py#L2013)
  : [example](http://nsls-ii.github.io/bluesky/plans.html#scans-over-one-dimesion)

## *Movable* & *Readable*

[*Movable* & *Readable*](https://github.com/NSLS-II/bluesky/blob/master/bluesky/run_engine.py#L488) 
are traits of detectors and positioners, respectively.

note:  There is reference to a *Flyable* but that is not defined in
[`bluesky.global_state`](https://github.com/NSLS-II/bluesky/blob/master/bluesky/global_state.py).

# Reference

## Example *documents*

For this BlueSky command:

    In [3]: RE(count([noisy], num=5), LiveTable(['noisy',]), comment='Hi, Jeff')
    Transient Scan ID: 7
    Persistent Unique Scan ID: '47a29b0a-2f54-4569-9692-28cbb0e59a21'
    +-----------+------------+------------+
    |   seq_num |       time |      noisy |
    +-----------+------------+------------+
    |         1 | 10:18:29.5 |    9.85723 |
    |         2 | 10:18:29.5 |    9.85723 |
    |         3 | 10:18:29.5 |    9.85723 |
    |         4 | 10:18:29.5 |    9.85723 |
    |         5 | 10:18:29.5 |    9.91683 |
    +-----------+------------+------------+
    generator count ['47a29b'] (scan num: 7)
    ['descriptors', 'start', 'stop']
    wrote: /home/oxygen18/JEMIAN/Documents/gov_7.h5
    Out[3]: ['47a29b0a-2f54-4569-9692-28cbb0e59a21']

these BlueSky `documents` are examples

### `descriptor`

    {
        "uid": "e1674f1a-948d-460b-ba83-bb3ac41d1c60",
        "configuration": {
            "noisy": {
                "data": {
                    "noisy": 9.85723175110278
                },
                "timestamps": {
                    "noisy": 1490714309.384322
                },
                "data_keys": {
                    "noisy": {
                        "shape": [],
                        "lower_ctrl_limit": 0,
                        "precision": 5,
                        "upper_ctrl_limit": 0,
                        "dtype": "number",
                        "source": "PV:gov:userCalc1",
                        "units": ""
                    }
                }
            }
        },
        "name": "primary",
        "run_start": "47a29b0a-2f54-4569-9692-28cbb0e59a21",
        "data_keys": {
            "noisy": {
                "shape": [],
                "lower_ctrl_limit": 0,
                "precision": 5,
                "object_name": "noisy",
                "upper_ctrl_limit": 0,
                "dtype": "number",
                "source": "PV:gov:userCalc1",
                "units": ""
            }
        },
        "_id": "58da7ec54843956977719ad8",
        "time": 1490714309.5471988,
        "object_keys": {
            "noisy": [
                "noisy"
            ]
        }
    }

### `event`

    {
        "uid": "f435c007-0954-4174-a64f-d4b4950db271",
        "data": {
            "noisy": 9.916828704464667
        },
        "timestamps": {
            "noisy": 1490714309.584365
        },
        "_id": "58da7ec54843956977719add",
        "time": 1490714309.5880601,
        "descriptor": "e1674f1a-948d-460b-ba83-bb3ac41d1c60",
        "seq_num": 5
    }
    {
        "uid": "d347f41a-bce8-4d96-b349-9998e369f167",
        "data": {
            "noisy": 9.85723175110278
        },
        "timestamps": {
            "noisy": 1490714309.384322
        },
        "_id": "58da7ec54843956977719adc",
        "time": 1490714309.5804646,
        "descriptor": "e1674f1a-948d-460b-ba83-bb3ac41d1c60",
        "seq_num": 4
    }
    {
        "uid": "24d6d808-23e3-4d27-8de1-4a74b149b894",
        "data": {
            "noisy": 9.85723175110278
        },
        "timestamps": {
            "noisy": 1490714309.384322
        },
        "_id": "58da7ec54843956977719adb",
        "time": 1490714309.5727956,
        "descriptor": "e1674f1a-948d-460b-ba83-bb3ac41d1c60",
        "seq_num": 3
    }
    {
        "uid": "9cfe1905-9061-4aab-a6c1-5fefd99c8232",
        "data": {
            "noisy": 9.85723175110278
        },
        "timestamps": {
            "noisy": 1490714309.384322
        },
        "_id": "58da7ec54843956977719ada",
        "time": 1490714309.5644457,
        "descriptor": "e1674f1a-948d-460b-ba83-bb3ac41d1c60",
        "seq_num": 2
    }
    {
        "uid": "e662c60f-8249-47f6-a12d-351fefe6a3fa",
        "data": {
            "noisy": 9.85723175110278
        },
        "timestamps": {
            "noisy": 1490714309.384322
        },
        "_id": "58da7ec54843956977719ad9",
    "time": 1490714309.5568695,
    "descriptor": "e1674f1a-948d-460b-ba83-bb3ac41d1c60",
    "seq_num": 1
}

### `start`

    {
        "login_id": "jemian@gov.aps.anl.gov",
        "plan_type": "generator",
        "EPICS_BASE": "/APSshare/epics/extensions-base/3.14.12.3-ext1",
        "beamline_id": "gov",
        "EPICS_DISPLAY_PATH": "/usr/local/iocapps/adlsys:/usr/local/iocapps/adlsys/temp",
        "detectors": [
            "noisy"
        ],
        "EPICS_TS_MIN_WEST": "360",
        "EPICS_CA_AUTO_ADDR_LIST": "yes",
        "plan_name": "count",
        "num_steps": 5,
        "uid": "47a29b0a-2f54-4569-9692-28cbb0e59a21",
        "EPICS_CA_ADDR_LIST": "164.54.124.4",
        "EPICS_EXTENSIONS": "/APSshare/epics/extensions",
        "EPICS_AR_PORT": "7002",
        "plan_args": {
            "num": 5,
            "detectors": [
                "EpicsSignalRO(read_pv='gov:userCalc1', name='noisy', value=9.85723175110278, timestamp=1490714309.384322, pv_kw={}, auto_monitor=False, string=False)"
            ]
        },
        "EPICS_HOST_ARCH": "linux-x86_64",
        "comment": "Hi, Jeff",
        "_id": "58da7ec54843956977719ad7",
        "EPICS_CA_MAX_ARRAY_BYTES": "2500000",
        "time": 1490714309.530326,
        "scan_id": 7,
        "EPICS_BASE_PVT": "/APSshare/epics/extensions-base/3.14.12.3-ext1"
    }

### `stop`

    {
        "uid": "6e25e54e-2482-4ef7-bbe3-54eaf69e5701",
        "run_start": "47a29b0a-2f54-4569-9692-28cbb0e59a21",
        "_id": "58da7ec54843956977719ade",
        "time": 1490714309.5924358,
        "exit_status": "success"
    }
