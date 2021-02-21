# Templates

Files and directories here are templates for installation.

It is assumed you have already [created a custom conda
environment](/install/README.md#activate-conda-base-environment) for your use of
the Bluesky framework.

CONTENTS

- [Templates](#templates)
- [Install instrument package](#install-instrument-package)
  - [ipython profile configuration](#ipython-profile-configuration)
  - [independent package installed into python environment](#independent-package-installed-into-python-environment)
  - [direct python code](#direct-python-code)
  - [happi database](#happi-database)
  - [configuration from YAML files](#configuration-from-yaml-files)
- [Install bluesky starter script](#install-bluesky-starter-script)
- [Revision control](#revision-control)

# Install instrument package

Configuration of a scientific instrument for Bluesky can be any of these methods:

1. [ipython profile configuration](#ipython-profile-configuration) -- typical for APS beam lines
1. [independent package installed into python environment](#independent-package-installed-into-python-environment)
1. [direct python code](#direct-python-code)
1. [happi](https://pcdshub.github.io/happi) database
1. [configuration from YAML files](configuration-from-YAML-files)

Note the older method of defining the instrument in the
[ipython profile](https://ipython.readthedocs.io/en/stable/config/intro.html#profiles)
using number files is deprecated as it quickly becomes difficult to manage
a typical instrument at a beam line.  Rather than use numbered files, read below to
install the instrument package into an ipython profile.

No matter which method you pick, you are **encouraged strongly** to place your
instrument package into a [revision control
system](https://github.com/BCDA-APS/use_bluesky/wiki#aps-list).

## ipython profile configuration

This is the most common installation for APS instruments.  It works well
for IPython console sessions.  It is slightly more difficult to use (than the
independent package installation) for Jupyter notebook sessions since the path
to the instrument package must be defined within the Jupyter session.

See the [installation guide](/install/README.md).

<details>
<summary>Example (TODO: NEEDS REVISION!)</summary>

2021-02-21 -- The new installation requires these instructions to be re-written.

```
(base) jemian@wow ~/.ipython/profile_testing $ ./install_startup.sh 45ID WNI wnicat
Extracting instrument package template: '/home/beams1/JEMIAN/.ipython/profile_bluesky/2021_1_startup.tar.gz'
Installing to IPython profile directory: '/home/beams1/JEMIAN/.ipython/profile_bluesky'
setting beam line name: 45ID
setting instrument name: WNI
setting databroker catalog: wnicat
editing starter shell script: /home/beams1/JEMIAN/.ipython/profile_bluesky/startup/blueskyStarter.sh
IPython directory: /home/beams1/JEMIAN/.ipython
IPython profile: testing
```

It's a good idea to soft link the starter script `blueskyStarter.sh` into
the `~/bin` directory (or some directory on the exectuable PATH) with a name
that shows the instrument it provides.

    cd ~/bin
    ln -s /home/beams1/JEMIAN/.ipython/profile_bluesky/startup/blueskyStarter.sh ./blueskyWNI.sh

NOTE:  If you do not have an Anaconda python distribution on path
`/APSshare/anaconda3/x86_64`, you will need to change the
`CONDA_ACTIVATE` variable in `startup/blueskyStarter.sh` to fit your system.

</details>

## independent package installed into python environment

From experience, we've learned that configuration of a scientific instrument
for the Bluesky framework is well-described as a Python package.  Both
[USAXS](https://github.com/APS-USAXS/ipython-usaxs/tree/main/profile_bluesky/startup/instrument)
and [XPCS](https://github.com/aps-8id-dys/ipython-8idiuser/tree/main/profile_bluesky/startup/instrument)
instruments are good examples.  The python package layout lends itself
to an intuitive description of the instrument into its component parts.  Here
is the basic layout:

```
    instrument/         # the instrument package
        session_logs    # setup log files
        framework/      # setup the Bluesky framework
        devices/        # define the ophyd (hardware AND software) devices
        callbacks/      # define any code to be called from the Run Engine (or other)
        plans/          # procedures custom to the instrument
        other/          # could be `utils` instead
```

<details>
<summary>Example (TODO: NEEDS REVISION!)</summary>

2021-02-21 -- The new installation requires these instructions to be re-written.

Use these bash commands to download and install the instrument package
template as an independent source code directory.

```
bash
mkdir ~/bluesky    # or your directory of choice
cd ~/bluesky
export URL=https://raw.githubusercontent.com/BCDA-APS/use_bluesky/main/templates/
wget ${URL}/instrument_template.tar.gz
tar xzf instrument_template.tar.gz
/bin/rm  -rf instrument_template.tar.gz
mv ./instrument_template/instrument .
mv ./instrument_template/setup.py .
mv ./instrument_template/README.md .
mv instrument_template/blueskyStarter.sh ~/bin/blueskyStarter.sh
/bin/rm -rf instrument_template
conda activate bluesky_2020_9
pip install -e .
```

</details>

## direct python code

Sometimes, such as for demos or exectuable scripts, the instrument
(or parts) are declared directly in the python code.  See the
[lessons](/lessons/README.md) in this repository for examples.

## happi database

[HAPPI](https://pcdshub.github.io/happi) is a database (using
[YAML](https://yaml.org/) files) for keeping track of
devices / configuration and fabricating ophyd (and pydm or other) objects on demand.

Configuration of a scientific instrument from a happi database is
under development at this time.  It's too early to document this now.

## configuration from YAML files

The APS HT-HEDM instrument has developed their own YAML
format to configure parts of the instrument, such as for
[tomography](https://github.com/aps-ht-hedm/jupyter-ht-hedm/blob/master/seisidd/config/tomo_devices.yml).  Consult this team for more information


# Install bluesky starter script

It is useful to create a bash shell script to start a bluesky
console session.  The shell script can define environment variables
needed only by this session.  See the example shell script
[`blueskyStarter.sh`](/templates/example_blueskyStarter.sh) in this directory.

Follow this guide to [install](/install.README.md#install-starter-script) a
starter script.

# Revision control

You are **encouraged strongly** to place your instrument package
into a revision control system such as git.  Compare with this
[table](https://github.com/BCDA-APS/use_bluesky/wiki#aps-list) of
other bluesky instruments at the APS.
