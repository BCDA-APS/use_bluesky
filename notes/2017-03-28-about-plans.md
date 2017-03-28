# Overview: What is a BlueSky *plan*?

In [BlueSky](https://github.com/NSLS-II/bluesky), all activity happens by the execution of a *plan*.
A BlueSky *plan* is a Python function that calls a sequence of BlueSky *messages* which
constitute data acquisition operations 
such as a scan or even the collection of a single value, such as counting from a scaler.

The BlueSky documentation provides and [introduction](http://nsls-ii.github.io/bluesky/plans_intro.html)
to [plans](http://nsls-ii.github.io/bluesky/plans.html).
This document expands to describe more details about BlueSky *plans*.

Many of the NSLS-II beam lines [store their configurations in 
GitHub](https://github.com/search?p=4&q=NSLS-II-&type=Repositories&utf8=%E2%9C%93).
The [custom *plans*](https://github.com/NSLS-II-XPD/ipython_ophyd/blob/master/profile_collection/startup/90-plans.py)
for the XPD instrument can be used as examples.

**summary**: 

* *plan* : Python command that executes a sequence of *messages*.
* *message* : instance of [`bluesky.utils.Msg`](https://github.com/NSLS-II/bluesky/blob/master/bluesky/utils.py#L23).
   syntax: `Msg(command, obj, *args, **kwargs)`

## The BlueSky *Run Engine*

To understand the BlueSky *plan*, it is first necessary to understand in what context
a plan is used.

The *RunEngine* is a state machine (states: idle, running, paused), 
reponsible for executing a *plan*.  It will emit a stream of BlueSky *documents*
as it executes the plan.  *The Run Engine executes messages and emits Documents.*
(A *document* is the fundamental record of storage in the BlueSky datastore.  It is a 
[json](http://json.org/) string.)  Each and every BlueSky *document* has its own
unique [*uid*](https://en.wikipedia.org/wiki/Universally_unique_identifier).  
These are used to identify individual documents and coordinate related
documents.  (While quite long, they can usually be abbreviated to the first
seven characters which are probably unique.)

These documents will take one of these forms (see *Reference* section below for examples):

* `start` : first document of a *plan*, includes values of all metadata objects
* `descriptor`: details of this *plan* including initial values
* `event` : one record of data of a *plan*, includes uid of *descriptor* document
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

    In [4]: RE(count([noisy], num=5, delay=1), LiveTable(['noisy',]), comment='Hi, Jeff')
    Transient Scan ID: 8
    Persistent Unique Scan ID: '0c5017d1-80b6-491e-a660-d51b57c6ef38'
    +-----------+------------+------------+
    |   seq_num |       time |      noisy |
    +-----------+------------+------------+
    |         1 | 10:36:12.6 |    9.91278 |
    |         2 | 10:36:13.6 |    9.84153 |
    |         3 | 10:36:14.6 |    9.85545 |
    |         4 | 10:36:15.6 |    9.90464 |
    |         5 | 10:36:16.6 |    9.85591 |
    +-----------+------------+------------+
    generator count ['0c5017'] (scan num: 8)
    ['descriptors', 'start', 'stop']
    wrote: /home/oxygen18/JEMIAN/Documents/gov_8.h5
    Out[4]: ['0c5017d1-80b6-491e-a660-d51b57c6ef38']


these BlueSky `documents` are examples of the stream of documents 
(in chronological order) emitted by the *Run Engine* for this instance
of the `count()` plan:

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
        "uid": "0c5017d1-80b6-491e-a660-d51b57c6ef38",
        "EPICS_CA_ADDR_LIST": "164.54.124.4",
        "EPICS_EXTENSIONS": "/APSshare/epics/extensions",
        "EPICS_AR_PORT": "7002",
        "plan_args": {
            "num": 5,
            "detectors": [
                "EpicsSignalRO(read_pv='gov:userCalc1', name='noisy', value=9.914008858692377, timestamp=1490715372.584322, pv_kw={}, auto_monitor=False, string=False)"
            ]
        },
        "EPICS_HOST_ARCH": "linux-x86_64",
        "comment": "Hi, Jeff",
        "_id": "58da82ec4843956977719adf",
        "EPICS_CA_MAX_ARRAY_BYTES": "2500000",
        "time": 1490715372.6131995,
        "scan_id": 8,
        "EPICS_BASE_PVT": "/APSshare/epics/extensions-base/3.14.12.3-ext1"
    }

### `descriptor`

    {
        "uid": "6f73de9e-4847-49f9-9cae-9e16309c3301",
        "configuration": {
            "noisy": {
                "data": {
                    "noisy": 9.912777372647597
                },
                "timestamps": {
                    "noisy": 1490715372.584322
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
        "run_start": "0c5017d1-80b6-491e-a660-d51b57c6ef38",
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
    "_id": "58da82ec4843956977719ae0",
    "time": 1490715372.6301644,
    "object_keys": {
        "noisy": [
            "noisy"
        ]
    }
}

### `event`

    {
        "uid": "45ce7233-89a8-43ea-b23f-319f09436612",
        "data": {
            "noisy": 9.841530553948303
        },
        "timestamps": {
            "noisy": 1490715373.584348
        },
        "_id": "58da82ed4843956977719ae2",
        "time": 1490715373.648545,
        "descriptor": "6f73de9e-4847-49f9-9cae-9e16309c3301",
        "seq_num": 2
    }
    {
        "uid": "9c757c1a-070a-40e4-aa0a-43db9836615d",
        "data": {
            "noisy": 9.855448709240992
        },
        "timestamps": {
            "noisy": 1490715374.584376
        },
        "_id": "58da82ee4843956977719ae3",
        "time": 1490715374.6576793,
        "descriptor": "6f73de9e-4847-49f9-9cae-9e16309c3301",
        "seq_num": 3
    }
    {
        "uid": "6a421191-57e3-403b-98a0-ab79885acd2b",
        "data": {
            "noisy": 9.904639158623565
        },
        "timestamps": {
            "noisy": 1490715375.58433
        },
        "_id": "58da82ef4843956977719ae4",
        "time": 1490715375.667277,
        "descriptor": "6f73de9e-4847-49f9-9cae-9e16309c3301",
        "seq_num": 4
    }
    {
        "uid": "2384a6f0-d0c8-4503-a85b-ab186245c5a5",
        "data": {
            "noisy": 9.855910948773882
        },
        "timestamps": {
            "noisy": 1490715376.584365
        },
        "_id": "58da82f04843956977719ae5",
        "time": 1490715376.6761823,
        "descriptor": "6f73de9e-4847-49f9-9cae-9e16309c3301",
        "seq_num": 5
    }

### `stop`

    {
        "uid": "37f0d6d3-9e89-4089-8ffb-702f135423f9",
        "run_start": "0c5017d1-80b6-491e-a660-d51b57c6ef38",
        "_id": "58da82f14843956977719ae6",
        "time": 1490715377.6821551,
        "exit_status": "success"
    }
