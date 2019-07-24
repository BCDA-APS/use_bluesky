# Install a new conda environment

If you have an existing python installation with conda installed,
then you can create a custom conda environment for Bluesky.

**Quick Summary**

1. use `bash` shell
1. Install Anaconda or Miniconda
1. activate *any* conda environment (usually `base`)
1. create a `bluesky` environment: `bash ./create_bluesky_env.sh`
1. create python 2 & 3 environments: `bash ./create_py27_py37_env.sh`

**Contents**

* [Does the bluesky environment exist already?](#does-the-bluesky-environment-exist-already)
* [What packages to install? -- The `requirements.txt` file](#what-packages-to-install--the-requirementstxt-file)
* [Where to get the packages? -- conda *channels*](#where-to-get-the-packages----conda-channels)
* [Create the custom environment for Bluesky](#create-the-custom-environment-for-bluesky)
* [Activate the `bluesky` environment](#activate-the-bluesky-environment)
* [Install default channels](#install-default-channels)
* [Install version restrictions](#install-version-restrictions)
* [Test the installation](#test-the-installation)
* [Summary](#summary)

**NOTE:** You will need to use the `bash` shell for the commands
in this procedure.  If you get strange errors from the various
commands, check that you are using the `bash` shell first.
Here's some [help](https://stackoverflow.com/questions/3327013/how-to-determine-the-current-shell-im-working-on)
with that.

## Does the `bluesky` environment exist already?

first, check that there is not a conda environment already named `bluesky` with command:  `conda env list`

```
snow% which conda
/APSshare/anaconda/x86_64/bin/conda
snow% conda env list
# conda environments:
#
base                  *  /APSshare/anaconda/x86_64
                         /home/USERNAME/xicam2_py_VE
```

Good, we can proceed with commands to install a new custom conda environment named `bluesky`.

## What packages to install? -- The `requirements.txt` file

We need to tell the 
[`conda create`](https://conda.io/projects/conda/en/latest/commands/create.html) 
command which packages to install.
In some cases, we must restrict which versions to be considered.
Download the [`requirements.txt`](requirements.txt) file to a
local, temporary location.  We'll need this only once to install the
custom conda environment.

## Where to get the packages? -- conda *channels*

The `conda create` command consults a list of web sites (known as 
[*channels*](https://conda.io/projects/conda/en/latest/commands/create.html#Channel%20Customization))
for available packages.  The web site contains information about each package 
available.  The packages describe what other packages (and versions) must be
installed for that package to work.  So, while we may request only a small number
of packages to be installed, there may be many more packages installed due
to dependencies amongst the stated requirements.  

The initial set of channels includes `defaults` which is the channel 
of common packages assembled by Anaconda.  The `python` package is one of these.
You can find many of the other channels at https://anaconda.org.

We will need more channels to support Bluesky.  Here is the (currently) recommended list:

	channels:
	  - defaults
	  - conda-forge
	  - lightsource2-tag
	  - aps-anl-tag

The version of EPICS support that we want is available on the `conda-forge` channel.
The main Bluesky packages are on `lightsource2-tag` while additional support for the
APS is on the `aps-anl-tag` channel.

## Create the custom environment for Bluesky

We'll create a new custom conda environment and give it the name *bluesky* 
(the [`-n bluesky`](https://conda.io/projects/conda/en/latest/commands/create.html#Target%20Environment%20Specification) 
part in the command).  Also, we'll specify each of the
*channels* from which to find packages to install.  The channels are searched
in the order they are specified.  The final part of the command gives the 
`requirements.txt` which specifies the list of packages and versions to be installed.

    conda create -n bluesky \
        -c defaults \
        -c conda-forge \
        -c lightsource2-tag \
        -c aps-anl-tag \
        --file=requirements.txt

**NOTE:** You might first get a warning that conda needs to be updated on the server.
That's ok for now.

The command will work for a bit, sifting through the various dependencies
and their requirements.  It will present you with a list of the packages to be downloaded
and installed.  Unless you have other reasons, press `y` to accept the list and to
proceed with the installation.

We can customize our use of `conda` so these channels
will always be used.  See the section [*Install default channels*](#install-default-channels).

## Activate the `bluesky` environment

**TIP:** For more help about `activate`, see Step 2 
[here](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html?highlight=activate#managing-environments).

Unless we specify otherwise, we are using the `base` environment
(the python from the directory where we first installed the Anaconda 
distribution).  Since we just created the `bluesky` environment, let's check that
it is installed.

```
snow% conda env list
# conda environments:
#
base                  *  /APSshare/anaconda/x86_64
bluesky                  /home/USERNAME/.conda/envs/bluesky
                         /home/USERNAME/xicam2_py_VE
```

The `*` indicates which environment is currently activated (and will be used when
we type `python` on the command line).

To activate the `bluesky` environment (be sure to use a **bash** shell):

```
snow% source /APSshare/anaconda/x86_64/bin/activate 
_CONDA_ROOT=/APSshare/anaconda/x86_64: Command not found.
_CONDA_ROOT: Undefined variable.
snow% bash
bash-4.2$ source /APSshare/anaconda/x86_64/bin/activate bluesky
(bluesky) bash-4.2$ 
```

Could be faster if we already used bash and had *some* conda environment already activated:

    conda activate bluesky

## Install default channels

This is a good time to add some conda channels (web sites with software) 
for our upcoming downloads and maintenance.

First, we must learn where to place the file.  
The list of available conda environments provides the directory path for each.

```
snow% conda env list
# conda environments:
#
base                  *  /APSshare/anaconda/x86_64
bluesky                  /home/USERNAME/.conda/envs/bluesky
                         /home/USERNAME/xicam2_py_VE
```

The file must go in our environment's directory, at 
[`./.condarc`](https://docs.conda.io/projects/conda/en/latest/user-guide/configuration/sample-condarc.html?highlight=condarc)

```
touch /home/USERNAME/.conda/envs/bluesky/.condarc
# edit that file adding these lines
channels:
  - defaults
  - conda-forge
  - lightsource2-tag
  - aps-anl-tag
```


## Install version restrictions

Some packages require that other packages are restricted to certain versions.
We can record this information so that we do not inadvertently 
[`conda update`](https://conda.io/projects/conda/en/latest/commands/update.html)
to an unacceptable version.  The process is known as 
[**pinning**](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-pkgs.html?highlight=pinned#preventing-packages-from-updating-pinning).

Note in our requirements that the tornado package must be kept at the latest 
version *before* major version 5 (for example, see 
https://github.com/ContinuumIO/anaconda-issues/issues/8789).  
We imposed that at the installation but we want to keep it from being updated later.  
We'll add a `pinned` file to our conda environment to maintain that rule for 
us during updates.

First, we must learn where to place the file.  
The list of available conda environments provides the directory path for each.

```
snow% conda env list
# conda environments:
#
base                  *  /APSshare/anaconda/x86_64
bluesky                  /home/USERNAME/.conda/envs/bluesky
                         /home/USERNAME/xicam2_py_VE
```

The file must go in our environment's directory, at `./conda-meta/pinned`

```
touch /home/USERNAME/.conda/envs/bluesky/conda-meta/pinned
# edit that file adding just this next line
tornado<5
```

## Test the installation

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
<summary>... response ...</summary>
<p>
	
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

</p>
</details>

Current values are: `aps.read()`

<details>
<summary>... response ...</summary>
<p>

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

</p>
</details>

You can still test that *ophyd* is working without a set of EPICS PVs by using the
simulators provided in *ophyd*.

    import ophyd.sim
    sim = ophyd.sim.hw()

Now test some of the simulators as above:

<details>
<summary>... session ...</summary>
<p>

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

</p>
</details>

## Summary

The condensed summary of commands (your installation directories might look a little different).

These are the installation/configuration steps (only need them once).

```
bash
cd /tmp
# download the files we'll need
wget https://raw.githubusercontent.com/BCDA-APS/use_bluesky/master/python_installation/requirements.txt
wget https://raw.githubusercontent.com/BCDA-APS/use_bluesky/master/python_installation/pinned
wget https://raw.githubusercontent.com/BCDA-APS/use_bluesky/master/python_installation/.condarc

# create & install (-y means accept and proceed without asking)
CHANNELS="-c defaults -c conda-forge -c lightsource2-tag -c aps-anl-tag"
conda create -n bluesky -y $CHANNELS --file=requirements.txt

# install additional configurations
cp pinned /home/USERNAME/.conda/envs/bluesky/conda-meta/
cp .condarc /home/USERNAME/.conda/envs/bluesky/
```

These are things you do with every new terminal session to use Bluesky:

```
# choose your working directory
cd ~/

# use the bluesky environment
conda activate bluesky

# now test in an ipython session
ipython
# ipython command prompt now...

# if you have APS PVs available
import apstools.devices as APS_devices
aps = APS_devices.ApsMachineParametersDevice(name="aps")
# print the APS real-time information
aps.current.value
aps.summary()
aps.read()

# test with ophyd simulators
import ophyd.sim
sim = ophyd.sim.hw()
sim.motor.position
sim.motor.read()
sim.noisy_det.read()
sim.noisy_det.value
```
