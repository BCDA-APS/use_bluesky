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

TODO: keep?

Beam lines of the Advanced Photon Source have access to EPICS PVs that tell the storage
ring current and other real-time information from the facility.  These have been
gathered into a special device from the `apstools` package.  (If you are not
at the APS, then you will need to test with different `ophyd.EpicsSignal` objects
than shown here.  You'll also need access to one or more EPICS PVs.)

Now we can test if we have installed enough software to be useful.  Might still need more...

```
import apstools.devices as APS_devices
aps = APS_devices.ApsMachineParametersDevice(name="aps")
```

We need to wait for those PVs to connect.  Check that `aps.connected` returns `True` before continuing.  Test by looking at the APS storage ring current:

    aps.current.value

The complete structure is: `aps.summary()`

<details>
	
```
In [3]: aps.summary()                                                                                      
data keys (* hints)
-------------------
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
----------
operator_messages    ApsOperatorMessagesDevice('aps_operator_messages')

Unused attrs
------------

```

</details>

Current values are: `aps.read()`

<details>

```
In [8]: aps.read()                                                                                         
Out[8]: 
OrderedDict([('aps_current',
              {'value': 88.52652776860398, 'timestamp': 1562701828.753756}),
             ('aps_lifetime',
              {'value': 52.583085617905894, 'timestamp': 1562701826.753587}),
             ('aps_machine_status',
              {'value': 'USER OPERATIONS', 'timestamp': 1562331601.371168}),
             ('aps_operating_mode',
              {'value': 'Delivered Beam', 'timestamp': 1562500392.942352}),
             ('aps_shutter_permit',
              {'value': 'PERMIT', 'timestamp': 1562500392.940957}),
             ('aps_fill_number',
              {'value': 25.0, 'timestamp': 1562500392.94135}),
             ('aps_orbit_correction',
              {'value': 0.0, 'timestamp': 1562701594.270834}),
             ('aps_global_feedback',
              {'value': 'On', 'timestamp': 1562701594.553689}),
             ('aps_global_feedback_h',
              {'value': 'On', 'timestamp': 1562701594.553689}),
             ('aps_global_feedback_v',
              {'value': 'On', 'timestamp': 1562701594.553689}),
             ('aps_operator_messages_operators',
              {'value': 'Dee Weyer and Steven LaBuda',
               'timestamp': 1562677538.647096}),
             ('aps_operator_messages_floor_coordinator',
              {'value': 'Shane Flood (2-0101)',
               'timestamp': 1562677404.908362}),
             ('aps_operator_messages_fill_pattern',
              {'value': '0+324x1 RHB', 'timestamp': 1561382181.863053}),
             ('aps_operator_messages_last_problem_message',
              {'value': '', 'timestamp': 1562500477.95326}),
             ('aps_operator_messages_last_trip_message',
              {'value': '', 'timestamp': 1562586730.877042}),
             ('aps_operator_messages_message6',
              {'value': 'Scheduled Fill on Fill at 07:45 & 19:45',
               'timestamp': 1562500507.033807}),
             ('aps_operator_messages_message7',
              {'value': '', 'timestamp': 1558051460.483074}),
             ('aps_operator_messages_message8',
              {'value': '', 'timestamp': 1558051455.619456})])

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
