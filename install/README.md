# Installation

Follow these sections, in sequence, to install the Bluesky framework for an instrument.

- [Installation](#installation)
  - [Activate Conda base Environment](#activate-conda-base-environment)
  - [Install Bluesky Environment](#install-bluesky-environment)
  - [Activate Bluesky Environment](#activate-bluesky-environment)
  - [Create IPython Profile for Bluesky](#create-ipython-profile-for-bluesky)
  - [Install Databroker Configuration File](#install-databroker-configuration-file)
  - [Install Instrument Package](#install-instrument-package)
  - [Commit Instrument Package to Version Control](#commit-instrument-package-to-version-control)
  - [Translate Previous SPEC Configuration](#translate-previous-spec-configuration)
  - [Add Environment Configuration to .bash_aliases](#add-environment-configuration-to-bash_aliases)
  - [Install Starter Script](#install-starter-script)
  - [Try it](#try-it)
    - [Test Existing Configuration](#test-existing-configuration)
      - [Read](#read)
      - [Move](#move)
      - [Count](#count)
      - [List, Describe, Summary](#list-describe-summary)
    - [Next Steps](#next-steps)
      - [Add Motor(s)](#add-motors)
      - [Add Scaler(s)](#add-scalers)
      - [Re-organize into Devices](#re-organize-into-devices)
      - [Add Area Detector(s)](#add-area-detectors)
      - [Other Device Support](#other-device-support)
      - [Implement Custom Plans](#implement-custom-plans)
      - [Review Metadata](#review-metadata)

## Activate Conda base Environment

TODO: install miniconda or anaconda

## Install Bluesky Environment

## Activate Bluesky Environment

## Create IPython Profile for Bluesky

## Install Databroker Configuration File

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


## Install Instrument Package

## Commit Instrument Package to Version Control

## Translate Previous SPEC Configuration

## Add Environment Configuration to .bash_aliases

## Install Starter Script

## Try it

* Change to desired working directory.
* Start Bluesky session using the starter script.

### Test Existing Configuration

* Verify the existing configuration works as expected:

  * motors have values matching EPICS
  * scaler(s) match EPICS

#### Read

command | description
--- | ---
`OBJECT.get()` | low-level command to show value of ophyd *Signal* named `OBJECT`
`OBJECT.read()` | data acquisition command, includes timestamp
`listdevice(OBJECT)` | table-version of `.read()`
`OBJECT.summary()` | more information about `OBJECT`
`MOTOR.position` | get readback, only for motor objects
`MOTOR.user_readback.get()` | alternative to `MOTOR.position`

#### Move

command | description
--- | ---
`%mov MOTOR value` | move MOTOR to value (command line only)
`%movr MOTOR value` | relative move (command line only)
`MOTOR.move(value)` | alternative to `%mov`
`MOTOR.user_setpoint.put(value)` | alternative to `%mov`

#### Count

command | description
--- | ---
`%ct` | 
TODO: OTHER | 

Count time setting is different for various types of detectors:

detector | set count time
--- | ---
scaler | `SCALER.preset_time.put(COUNT_TIME_S)`
area detector | `AD.cam.acquire_time.put(COUNT_TIME_S)`

#### List, Describe, Summary

command | description
--- | ---
`wa` | show all labeled objects
`listobjects()` | table of all global objects
`listruns()` | table of runs (default: last 20)
`OBJECT.describe()` | 

### Next Steps

#### Add Motor(s)

#### Add Scaler(s)

#### Re-organize into Devices

#### Add Area Detector(s)

#### Other Device Support

#### Implement Custom Plans

#### Review Metadata
