# Installation

Follow these sections, in sequence, to install the Bluesky framework for an
instrument.

- [Installation](#installation)
  - [Activate Conda "base" Environment](#activate-conda-base-environment)
  - [Install Databroker Configuration File](#install-databroker-configuration-file)
  - [Install Bluesky Environment](#install-bluesky-environment)
  - [Activate Bluesky Environment](#activate-bluesky-environment)
  - [Create IPython Profile for Bluesky](#create-ipython-profile-for-bluesky)
  - [Install Instrument Package](#install-instrument-package)
  - [Commit Instrument Package to Version Control](#commit-instrument-package-to-version-control)
  - [Translate Previous SPEC Configuration](#translate-previous-spec-configuration)
  - [Add Environment Configuration to .bash_aliases](#add-environment-configuration-to-bash_aliases)
  - [Install Starter Script](#install-starter-script)
  - [Start Bluesky](#start-bluesky)

Once installed, proceed to these guides:

* Test your installation following the [First Steps Guide](first_steps_guide.md)
* Continue building the instrument package following the [Instrument Package Guide](instrument_package_guide.md)

## Activate Conda "base" Environment

TODO: install miniconda or anaconda

## Install Databroker Configuration File

This file configures how Bluesky connects with its repository (and databases) on
the MongoDB database server.

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

The beam line controls group (BCDA) will assign the REPOSITORY and its SERVER.

## Install Bluesky Environment

Get the installation configuration ([YAML](https://yaml.org)) file.  The file is
versioned based on the APS run cycle.  This YAML file is for the first run
(January-April) in 2021.

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

## Create IPython Profile for Bluesky

If there is an existing `~/.ipython` directory (perhaps created for other use
from this account), then choose a unique directory for bluesky.  Typical
alternative is `~/.ipython-bluesky`.

```
export BLUESKY_DIR=~/.ipython
ipython profile create bluesky --ipython-dir="${BLUESKY_DIR}"
```


## Install Instrument Package

Remove the existing `startup` directory (created from `ipython profile create` step above):

```
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

The beam line controls group (BCDA) will assign the REPOSITORY and its SERVER.


## Commit Instrument Package to Version Control

## Translate Previous SPEC Configuration

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
