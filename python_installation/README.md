# Install a new conda environment

If you have an existing python installation with conda installed,
then you can create a custom conda environment for Bluesky.

**Contents**

- [Install a new conda environment](#install-a-new-conda-environment)
  - [Quick Summary](#quick-summary)
    - [Use bash shell](#use-bash-shell)
  - [Create IPython profile for Bluesky](#create-ipython-profile-for-bluesky)
  - [Setup custom environment for Bluesky](#setup-custom-environment-for-bluesky)
  - [Test the installation](#test-the-installation)

## Quick Summary

1. [Install Anaconda or Miniconda](miniconda.md)
1. use `bash` shell
1. Create IPython profile for bluesky
1. activate *any* conda environment (usually `base`)
1. create environment for `bluesky`: `bash ./setup_2020_5.sh`

### Use bash shell

**NOTE:** You will need to use the `bash` shell for the commands
in this procedure.  If you get strange errors from the various
commands, check that you are using the `bash` shell first.
Here's some [help](https://stackoverflow.com/questions/3327013/how-to-determine-the-current-shell-im-working-on)
with that.

## Create IPython profile for Bluesky

If there is no `~/.ipython` directory (or the existing one contains only the
default configuration), then:

    ipython profile create bluesky

Otherwise, create a new directory for use with Bluesky and ipython.
Pick a directory name not already in use, such as `~/.ipython-bluesky`,
then:

    ipython profile create bluesky --ipython-dir=~/.ipython-bluesky

## Setup custom environment for Bluesky

Run: `bash ./setup_2020_5.sh`

Since the toolset for running bluesky is under continuous development,
the best recommendations change as new software is released.

The installer will create a new custom conda environment 
and give it a calendar-based name, such as *bluesky_2020_5* .
This will preserve previously installed bluesky environments as fallbacks.

**NOTE:** You might first get a warning that conda needs to be updated on the server.
That's ok for now.

The command will work for a bit, sifting through the various dependencies
and their requirements.  It will present you with a list of the packages to be downloaded
and installed.  Unless you have other reasons, press `y` to accept the list and to
proceed with the installation.


## Test the installation

Beam lines of the Advanced Photon Source have access to EPICS PVs that tell the storage
ring current and other real-time information from the facility.  These have been
gathered into a special device from the `apstools` package.  (If you are not
at the APS, then you will need to test with different `ophyd.EpicsSignal` objects
than shown here.  You'll also need access to one or more EPICS PVs.)

Now we can test if we have installed enough software to be useful.  Might still need more...

```
from apstools.devices import ApsMachineParametersDevice
aps = ApsMachineParametersDevice(name="aps")
```

We need to wait for those PVs to connect (could call `aps.wait_for_connections()`).
Check that `aps.connected` returns `True` before continuing.  Test by looking at the
APS storage ring current:

    aps.current.value

The complete structure:

<details>
<summary><tt>aps.summary()</tt></summary>

```
In [1]: aps.summary()                                                                                                   
data keys (* hints)
-------------------
 aps_aps_cycle
 aps_current
 aps_fill_number
 aps_global_feedback
 aps_global_feedback_h
 aps_global_feedback_v
 aps_lifetime
 aps_machine_status
 aps_operating_mode
 aps_operator_messages_fill_pattern
 aps_operator_messages_floor_coordinator
 aps_operator_messages_last_problem_message
 aps_operator_messages_last_trip_message
 aps_operator_messages_message6
 aps_operator_messages_message7
 aps_operator_messages_message8
 aps_operator_messages_operators
 aps_orbit_correction
 aps_shutter_permit

read attrs
----------
current              EpicsSignalRO       ('aps_current')
lifetime             EpicsSignalRO       ('aps_lifetime')
aps_cycle            ApsCycleComputedRO  ('aps_aps_cycle')
machine_status       EpicsSignalRO       ('aps_machine_status')
operating_mode       EpicsSignalRO       ('aps_operating_mode')
shutter_permit       EpicsSignalRO       ('aps_shutter_permit')
fill_number          EpicsSignalRO       ('aps_fill_number')
orbit_correction     EpicsSignalRO       ('aps_orbit_correction')
global_feedback      EpicsSignalRO       ('aps_global_feedback')
global_feedback_h    EpicsSignalRO       ('aps_global_feedback_h')
global_feedback_v    EpicsSignalRO       ('aps_global_feedback_v')
operator_messages    ApsOperatorMessagesDevice('aps_operator_messages')
operator_messages.operators EpicsSignalRO       ('aps_operator_messages_operators')
operator_messages.floor_coordinator EpicsSignalRO       ('aps_operator_messages_floor_coordinator')
operator_messages.fill_pattern EpicsSignalRO       ('aps_operator_messages_fill_pattern')
operator_messages.last_problem_message EpicsSignalRO       ('aps_operator_messages_last_problem_message')
operator_messages.last_trip_message EpicsSignalRO       ('aps_operator_messages_last_trip_message')
operator_messages.message6 EpicsSignalRO       ('aps_operator_messages_message6')
operator_messages.message7 EpicsSignalRO       ('aps_operator_messages_message7')
operator_messages.message8 EpicsSignalRO       ('aps_operator_messages_message8')

config keys
-----------

configuration attrs
-------------------
operator_messages    ApsOperatorMessagesDevice('aps_operator_messages')

unused attrs
------------

```

</details>

Current values are: `aps.read()`

<details>
<summary><tt>aps.read()</tt></summary>

```
In [2]: aps.read()                                                                                                      
Out[2]: 
OrderedDict([('aps_current',
              {'value': 74.90453756160933, 'timestamp': 1595343111.512742}),
             ('aps_lifetime',
              {'value': 13.004700442180901, 'timestamp': 1595343111.356158}),
             ('aps_aps_cycle',
              {'value': '2020-2', 'timestamp': 1595343077.3078227}),
             ('aps_machine_status',
              {'value': 'ASD Studies', 'timestamp': 1595250001.449054}),
             ('aps_operating_mode',
              {'value': 'Stored Beam', 'timestamp': 631152000.0}),
             ('aps_shutter_permit',
              {'value': 'NO PERMIT', 'timestamp': 1595250006.403736}),
             ('aps_fill_number', {'value': 11.0, 'timestamp': 631152000.0}),
             ('aps_orbit_correction',
              {'value': 0.0, 'timestamp': 631152000.0}),
             ('aps_global_feedback',
              {'value': 'On', 'timestamp': 631152000.0}),
             ('aps_global_feedback_h',
              {'value': 'On', 'timestamp': 631152000.0}),
             ('aps_global_feedback_v',
              {'value': 'On', 'timestamp': 631152000.0}),
             ('aps_operator_messages_operators',
              {'value': 'LaBuda, Kimbro', 'timestamp': 1595336092.424329}),
             ('aps_operator_messages_floor_coordinator',
              {'value': 'Clay White (2-0101)',
               'timestamp': 1595336094.220797}),
             ('aps_operator_messages_fill_pattern',
              {'value': '', 'timestamp': 1595278298.418265}),
             ('aps_operator_messages_last_problem_message',
              {'value': '', 'timestamp': 1595247250.36637}),
             ('aps_operator_messages_last_trip_message',
              {'value': '', 'timestamp': 1595247255.006215}),
             ('aps_operator_messages_message6',
              {'value': 'User Operations at 08:00 Wed. 7/22',
               'timestamp': 1595336103.81407}),
             ('aps_operator_messages_message7',
              {'value': '', 'timestamp': 1591647283.478823}),
             ('aps_operator_messages_message8',
              {'value': '', 'timestamp': 1591647284.846647})])

```

</details>

Current values are: `aps.read()`

<details>
<summary>as table: <tt>device_read2table(aps)</tt></summary>

```
In [4]: from apstools.utils import device_read2table                                                                    

In [5]: device_read2table(aps)                                                                                          
========================================== ================================== ==========================
name                                       value                              timestamp                 
========================================== ================================== ==========================
aps_current                                74.82578332160934                  2020-07-21 09:52:40.512772
aps_lifetime                               13.921180095258897                 2020-07-21 09:52:36.356164
aps_aps_cycle                              2020-2                             2020-07-21 09:51:17.307823
aps_machine_status                         ASD Studies                        2020-07-20 08:00:01.449054
aps_operating_mode                         Stored Beam                        1989-12-31 18:00:00       
aps_shutter_permit                         NO PERMIT                          2020-07-20 08:00:06.403736
aps_fill_number                            11.0                               1989-12-31 18:00:00       
aps_orbit_correction                       0.0                                1989-12-31 18:00:00       
aps_global_feedback                        On                                 1989-12-31 18:00:00       
aps_global_feedback_h                      On                                 1989-12-31 18:00:00       
aps_global_feedback_v                      On                                 1989-12-31 18:00:00       
aps_operator_messages_operators            LaBuda, Kimbro                     2020-07-21 07:54:52.424329
aps_operator_messages_floor_coordinator    Clay White (2-0101)                2020-07-21 07:54:54.220797
aps_operator_messages_fill_pattern                                            2020-07-20 15:51:38.418265
aps_operator_messages_last_problem_message                                    2020-07-20 07:14:10.366370
aps_operator_messages_last_trip_message                                       2020-07-20 07:14:15.006215
aps_operator_messages_message6             User Operations at 08:00 Wed. 7/22 2020-07-21 07:55:03.814070
aps_operator_messages_message7                                                2020-06-08 15:14:43.478823
aps_operator_messages_message8                                                2020-06-08 15:14:44.846647
========================================== ================================== ==========================

Out[5]: <pyRestTable.rest_table.Table at 0x7f3c0654a990>

```

</details>

You can still test that *ophyd* is working without a set of EPICS PVs by using the
simulators provided in *ophyd*.

    import ophyd.sim
    sim = ophyd.sim.hw()

Now test some of the simulators as above:

<details>

```
In [10]: sim.motor.position                                                                                                                                          
Out[10]: 0

In [11]: sim.motor.read()                                                                                                                                            
Out[11]: 
OrderedDict([('motor', {'value': 0, 'timestamp': 1562779985.5141134}),
             ('motor_setpoint',
              {'value': 0, 'timestamp': 1562779985.5141122})])

In [12]: sim.noisy_det.read()                                                                                                                                        
Out[12]: {'noisy_det': {'value': 0.9765596019916091, 'timestamp': 1562779985.5194004}}

In [13]: sim.noisy_det.value                                                                                                                                         
Out[13]: 0.9765596019916091

```

</details>
