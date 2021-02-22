# Installation

Follow these sections, in sequence, to install the Bluesky framework for an
instrument.


**Contents**
- [Installation](#installation)
  - [Activate Conda "base" Environment](#activate-conda-base-environment)
  - [Install MongoDB server](#install-mongodb-server)
  - [Install Databroker Configuration File](#install-databroker-configuration-file)
  - [Install Bluesky Environment](#install-bluesky-environment)
  - [Activate Bluesky Environment](#activate-bluesky-environment)
    - [Test that Bluesky Works](#test-that-bluesky-works)
  - [Create IPython Profile for Bluesky](#create-ipython-profile-for-bluesky)
  - [Install Instrument Package](#install-instrument-package)
  - [Commit Instrument Package to Version Control](#commit-instrument-package-to-version-control)
  - [Translate Previous SPEC Configuration](#translate-previous-spec-configuration)
  - [Add Environment Configuration to .bash_aliases](#add-environment-configuration-to-bash_aliases)
  - [Install Starter Script](#install-starter-script)
  - [Start Bluesky](#start-bluesky)

Once installed, proceed to these guides:

* Test your installation following the [First Steps Guide](../first_steps_guide.md)
* Continue building the instrument package following the [Instrument Package Guide](../instrument_package_guide.md)

**NOTE:** You will need to use the `bash` shell for the commands
in this guide.  If you get strange errors from the various
commands, check that you are using the `bash` shell first.
Here's some [advice](https://stackoverflow.com/questions/3327013/how-to-determine-the-current-shell-im-working-on) to determine the
current shell.


## Activate Conda "base" Environment

Look at the prompt in your Linux terminal.  If the first part (`(base)`)
looks like this example:

    (base) mintadmin@mint-vm:/tmp$ 

then you already have a base environment activated.  If your command
does not start like the example above, such as:

    mintadmin@mint-vm:/tmp$ 

you need to activate the base environment first.  You'll need to know
the path to an installation of Miniconda or Anaconda python.  (Follow
this [guide](miniconda.md) if you need to install Miniconda or
Anaconda.)

At APS, use this command:

    source /APSshare/miniconda/x86_64/bin/activate base

If you installed your own, then:

    source /path/to/miniconda3/bin/activate base

Once activated, you can see all installed environments with this command:

```
mintadmin@mint-vm:/tmp$ conda env list
# conda environments:
#
base                  *  /home/mintadmin/Apps/anaconda

```


## Install MongoDB server

If you need to provide your own MongoDB server, follow this
[guide](https://github.com/BCDA-APS/use_bluesky/wiki/mongodb-server).

At the APS, the beam line controls group (BCDA) will assign the
REPOSITORY and its SERVER.

## Install Databroker Configuration File

This file configures how Bluesky connects with its repository (and
databases) on the MongoDB database server.

Follow this template:

```
sources:
  REPOSITORY:
    args:
      asset_registry_db: mongodb://SERVER:27017/REPOSITORY-bluesky
      metadatastore_db: mongodb://SERVER:27017/REPOSITORY-bluesky
    driver: bluesky-mongo-normalized-catalog
```

Replace the `REPOSITORY` and `SERVER` terms and write to file:
`~/.local/share/intake/catalogs.yml`.

At the APS, the beam line controls group (BCDA) will assign the
REPOSITORY and its SERVER.

## Install Bluesky Environment

Get the installation configuration ([YAML](https://yaml.org)) file.  The
file is versioned based on the APS run cycle.  This YAML file is for the
first run (January-April) in 2021.

```
cd /tmp
wget https://github.com/BCDA-APS/use_bluesky/raw/main/install/environment_2021_1.yml
```

Create the custom conda environment named in the file (`bluesky_2021_1`):

```
conda env create -f environment_2021_1.yml
```

## Activate Bluesky Environment

```
conda activate bluesky_2021_1
```

### Test that Bluesky Works

Beam lines of the Advanced Photon Source have access to EPICS PVs that
tell the storage ring current and other real-time information from the
facility.  These have been gathered into a special device from the
`apstools` package.  (If you are not at the APS, then you will need to
test with different `ophyd.EpicsSignal` objects than shown here.  You'll
also need access to one or more EPICS PVs.)

Now we can test if we have installed enough software to be useful.
Might still need more...

```
from apstools.devices import ApsMachineParametersDevice
aps = ApsMachineParametersDevice(name="aps")
```

We need to wait for those PVs to connect (could call
`aps.wait_for_connections()`). Check that `aps.connected` returns `True`
before continuing.  Test by looking at the APS storage ring current:

    aps.current.value


<details>
<summary><tt>aps.summary()</tt>: complete structure</summary>

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


<details>
<summary><tt>aps.read()</tt>: current timestamped values</summary>

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


<details>
<summary><tt>device_read2table(aps): <tt>aps.read()</tt> in table with formatted timestamps</tt></summary>

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


<details>
<summary>Test some of the simulators (without EPICS)</summary>

You can still test that *ophyd* is working without a set of EPICS PVs by using the
simulators provided in *ophyd*.

    import ophyd.sim
    sim = ophyd.sim.hw()

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


## Create IPython Profile for Bluesky

If there is an existing `~/.ipython` directory (perhaps created for other use
from this account), then choose a unique directory for bluesky.  Typical
alternative is `~/.ipython-bluesky`.

```
export BLUESKY_DIR=~/.ipython
ipython profile create bluesky --ipython-dir="${BLUESKY_DIR}"
```


## Install Instrument Package

Remove the existing `startup` directory (created from `ipython profile
create` step above):

```
cd "${BLUESKY_DIR}/profile_bluesky"
rm startup/README
rmdir startup
```

Download the install script:

```
cd "${BLUESKY_DIR}/profile_bluesky"
wget https://github.com/BCDA-APS/use_bluesky/raw/main/install/install_startup.sh
```

Run the installer

```
bash ./install_startup.sh  BEAMLINE INSTRUMENT REPOSITORY
```

where `BEAMLINE` `INSTRUMENT` `REPOSITORY` each contain no white space
characters.  The terms BEAMLINE and INSTRUMENT will be added to the standard
metadata added to every Bluesky
[_run_](https://blueskyproject.io/bluesky/documents.html?highlight=run).
Example: `bash ./install_startup.sh  45-ID FemtoScanner 45id_femtoscanner`

At the APS, the beam line controls group (BCDA) will assign the
REPOSITORY and its SERVER.


## Commit Instrument Package to Version Control

Until this section is written, compare with other APS instruments
listed on the [wiki](https://github.com/BCDA-APS/use_bluesky/wiki).

<details>
<summary>TODO:</summary>

* identify or create GitHub organization
* create empty GitHub repository
* clone GitHub repository to the startup directory or .ipython
* adjust the .gitignore file
* add new content, commit, and push back to GitHub
* See the [wiki](https://github.com/BCDA-APS/use_bluesky/wiki) for details.
</details>

## Translate Previous SPEC Configuration

The [`apstools`]() package has an application that will translate most
of the SPEC config file into ophyd commands.  The output is to the
console.  Use a pipe to direct the output to a new file:

```
export INSTRUMENT=${BLUESKY_DIR}/profile/bluesky/startup/instrument
spec2ophyd CONFIG_FILE | tee ${INSTRUMENT}/devices/spec.py
```

then make sure to import this file in
`${INSTRUMENT}/devices/__init__.py` following the pattern of other
imports there.

<details>
<summary><tt>spec2ophyd</tt> example:</summary>

```
(bluesky_2021_1) mintadmin@mint-vm:/tmp$ spec2ophyd /home/mintadmin/Documents/projects/BCDA-APS/apstools/apstools/migration/config
"""
ophyd commands from SPEC config file

file: /home/mintadmin/Documents/projects/BCDA-APS/apstools/apstools/migration/config

CAUTION: Review the object names below before using them!
    Some names may not be valid python identifiers
    or may be reserved (such as ``time`` or ``del``)
    or may be vulnerable to re-definition because
    they are short or common.
"""

from ophyd import EpicsMotor, EpicsSignal
from ophyd.scaler import ScalerCH

un0 = EpicsMotor('9idcLAX:m58:c0:m1', name='un0', labels=('motor',))  # unused0
mx = EpicsMotor('9idcLAX:m58:c0:m2', name='mx', labels=('motor',))
my = EpicsMotor('9idcLAX:m58:c0:m3', name='my', labels=('motor',))
waxsx = EpicsMotor('9idcLAX:m58:c0:m4', name='waxsx', labels=('motor',))  # WAXS X
ax = EpicsMotor('9idcLAX:m58:c0:m5', name='ax', labels=('motor',))
gslity = EpicsMotor('9idcLAX:m58:c0:m6', name='gslity', labels=('motor',))  # Gslit_Y
az = EpicsMotor('9idcLAX:m58:c0:m7', name='az', labels=('motor',))
un7 = EpicsMotor('9idcLAX:m58:c0:m8', name='un7', labels=('motor',))  # unused7
msx = EpicsMotor('9idcLAX:m58:c1:m1', name='msx', labels=('motor',))
msy = EpicsMotor('9idcLAX:m58:c1:m2', name='msy', labels=('motor',))
art = EpicsMotor('9idcLAX:m58:c1:m3', name='art', labels=('motor',))  # ART50-100
asy = EpicsMotor('9idcLAX:m58:c1:m4', name='asy', labels=('motor',))
gslitx = EpicsMotor('9idcLAX:m58:c1:m5', name='gslitx', labels=('motor',))  # Gslit_X
tcam = EpicsMotor('9idcLAX:m58:c1:m6', name='tcam', labels=('motor',))
camy = EpicsMotor('9idcLAX:m58:c1:m7', name='camy', labels=('motor',))  # cam_y
tens = EpicsMotor('9idcLAX:m58:c1:m8', name='tens', labels=('motor',))  # Tension
sx = EpicsMotor('9idcLAX:m58:c2:m1', name='sx', labels=('motor',))
sy = EpicsMotor('9idcLAX:m58:c2:m2', name='sy', labels=('motor',))
dx = EpicsMotor('9idcLAX:m58:c2:m3', name='dx', labels=('motor',))
un19 = EpicsMotor('9idcLAX:m58:c2:m4', name='un19', labels=('motor',))
uslvcen = EpicsMotor('9idcLAX:m58:c2:m5', name='uslvcen', labels=('motor',))  # uslitvercen
uslhcen = EpicsMotor('9idcLAX:m58:c2:m6', name='uslhcen', labels=('motor',))  # uslithorcen
uslvap = EpicsMotor('9idcLAX:m58:c2:m7', name='uslvap', labels=('motor',))  # uslitverap
uslhap = EpicsMotor('9idcLAX:m58:c2:m8', name='uslhap', labels=('motor',))  # uslithorap
pin_x = EpicsMotor('9idcLAX:mxv:c0:m1', name='pin_x', labels=('motor',))
pin_z = EpicsMotor('9idcLAX:mxv:c0:m2', name='pin_z', labels=('motor',))
gslout = EpicsMotor('9idcLAX:mxv:c0:m3', name='gslout', labels=('motor',))  # GSlit_outb # read_mode=7
gslinb = EpicsMotor('9idcLAX:mxv:c0:m4', name='gslinb', labels=('motor',))  # GSlit_inb # read_mode=7
gsltop = EpicsMotor('9idcLAX:mxv:c0:m5', name='gsltop', labels=('motor',))  # GSlit_top # read_mode=7
gslbot = EpicsMotor('9idcLAX:mxv:c0:m6', name='gslbot', labels=('motor',))  # GSlit_bot # read_mode=7
un30 = EpicsMotor('9idcLAX:mxv:c0:m7', name='un30', labels=('motor',))  # unused30
pin_y = EpicsMotor('9idcLAX:mxv:c0:m8', name='pin_y', labels=('motor',))
a2rp = EpicsMotor('9idcLAX:pi:c0:m1', name='a2rp', labels=('motor',))  # USAXS.a2rp
m2rp = EpicsMotor('9idcLAX:pi:c0:m2', name='m2rp', labels=('motor',))  # USAXS.m2rp
msrp = EpicsMotor('9idcLAX:pi:c0:m3', name='msrp', labels=('motor',))  # USAXS.msrp
asrp = EpicsMotor('9idcLAX:pi:c0:m4', name='asrp', labels=('motor',))  # USAXS.asrp
un36 = EpicsMotor('9idcLAX:xps:c0:m1', name='un36', labels=('motor',))  # unused36
un37 = EpicsMotor('9idcLAX:xps:c0:m2', name='un37', labels=('motor',))  # unused37
mst = EpicsMotor('9idcLAX:xps:c0:m3', name='mst', labels=('motor',))
ast = EpicsMotor('9idcLAX:xps:c0:m4', name='ast', labels=('motor',))
msr = EpicsMotor('9idcLAX:xps:c0:m5', name='msr', labels=('motor',))
asr = EpicsMotor('9idcLAX:xps:c0:m6', name='asr', labels=('motor',))
un42 = EpicsMotor('9idcLAX:xps:c0:m7', name='un42', labels=('motor',))  # unused42
un43 = EpicsMotor('9idcLAX:xps:c0:m8', name='un43', labels=('motor',))  # unused43
ar = EpicsMotor('9idcLAX:aero:c0:m1', name='ar', labels=('motor',))
un45 = EpicsMotor('9idcLAX:mxv:c1:m1', name='un45', labels=('motor',))
un46 = EpicsMotor('9idcLAX:mxv:c1:m2', name='un46', labels=('motor',))
un47 = EpicsMotor('9idcLAX:mxv:c1:m3', name='un47', labels=('motor',))
un48 = EpicsMotor('9idcLAX:mxv:c1:m4', name='un48', labels=('motor',))
un49 = EpicsMotor('9idcLAX:mxv:c1:m5', name='un49', labels=('motor',))
un50 = EpicsMotor('9idcLAX:mxv:c1:m6', name='un50', labels=('motor',))
un51 = EpicsMotor('9idcLAX:mxv:c1:m7', name='un51', labels=('motor',))
un52 = EpicsMotor('9idcLAX:mxv:c1:m8', name='un52', labels=('motor',))
ay = EpicsMotor('9idcLAX:aero:c1:m1', name='ay', labels=('motor',))
dy = EpicsMotor('9idcLAX:aero:c2:m1', name='dy', labels=('motor',))
# Macro Motor: SpecMotor(mne='en', config_line='55', macro_prefix='kohzuE') # read_mode=7
InbMS = EpicsMotor('9ida:m43', name='InbMS', labels=('motor',))  # MonoSl_inb
OutMS = EpicsMotor('9ida:m44', name='OutMS', labels=('motor',))  # MonoSl_out
TopMS = EpicsMotor('9ida:m45', name='TopMS', labels=('motor',))  # MonoSl_top
BotMS = EpicsMotor('9ida:m46', name='BotMS', labels=('motor',))  # MonoSl_bot
mr = EpicsMotor('9idcLAX:aero:c3:m1', name='mr', labels=('motor',))
c0 = ScalerCH('9idcLAX:vsc:c0', name='c0', labels=('detectors',))
c0.select_channels(None)
sec = c0.channels.chan01.s
I0 = c0.channels.chan02.s
I00 = c0.channels.chan03.s
upd2 = c0.channels.chan04.s
trd = c0.channels.chan05.s
I000 = c0.channels.chan06.s
```

</details>

## Add Environment Configuration to .bash_aliases

The `~/.bash_aliases` file is the usual place to customize the bash shell.  It
is executed from `~/.bashrc` when a new console is created.

Add these lines to `~/.bash_aliases`:

```
export CONDA_ENVIRONMENT=bluesky_2021_1
alias become_bluesky='conda activate "${CONDA_ENVIRONMENT}" '
```

## Install Starter Script

It is useful to create a local directory (such as `~/bin`) for custom starter
scripts and executable file links.  Use these steps to configure your account.
Add this line to `~/.bash_aliases`:

```
export PATH="~/bin:${PATH}"
```

and create the directory:

```
mkdir ~/bin
```

Add the starter script to `~/bin`:

```
cd ~/bin
ln -s ${BLUESKY_DIR}/profile_bluesky/startup/blueskyStarter.sh ./
```

TIP: You might rename `~/bin/blueskyStarter.sh` to something appropriate for
your instrument name, such as the hypothetical example above:
`blueskyFemtoScanner.sh`

## Start Bluesky

* Change to desired working directory.
* Start Bluesky session using the starter script.
