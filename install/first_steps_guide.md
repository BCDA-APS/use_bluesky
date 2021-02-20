# First Steps Guide

* Verify the existing configuration works as expected:

  * motors have values matching EPICS
  * scaler(s) match EPICS

- [First Steps Guide](#first-steps-guide)
  - [Read](#read)
  - [Move](#move)
  - [Count](#count)
  - [List, Describe, Summary](#list-describe-summary)
  - [Log files](#log-files)

## Read

command | description
--- | ---
`OBJECT.get()` | low-level command to show value of ophyd *Signal* named `OBJECT`
`OBJECT.read()` | data acquisition command, includes timestamp
`listdevice(OBJECT)` | table-version of `.read()`
`OBJECT.summary()` | more information about `OBJECT`
`MOTOR.position` | get readback, only for motor objects
`MOTOR.user_readback.get()` | alternative to `MOTOR.position`

## Move

command | description
--- | ---
`%mov MOTOR value` | move MOTOR to value (command line only)
`%movr MOTOR value` | relative move (command line only)
`MOTOR.move(value)` | alternative to `%mov`
`MOTOR.user_setpoint.put(value)` | alternative to `%mov`

## Count

command | description
--- | ---
`%ct` |
TODO: OTHER |

Count time setting is different for various types of detectors:

detector | set count time
--- | ---
scaler | `SCALER.preset_time.put(COUNT_TIME_S)`
area detector | `AD.cam.acquire_time.put(COUNT_TIME_S)`

## List, Describe, Summary

command | description
--- | ---
`wa` | show all labeled objects
`listobjects()` | table of all global objects
`listruns()` | table of runs (default: last 20)
`OBJECT.describe()` | OBJECT metadata: PV, type, units, limits, precision, ... (written as part of a run)
`OBJECT.summary()` | OBJECT details in human readable terms

## Log files

In the working directory, the log files are written to a `./.logs` subdirectory.
There are two kinds of file, one that records user commands and the python
result, the other records items sent to the
[customized](https://github.com/prjemian/stdlogpj#example-directing-logs-to-a-specific-directory)
Python [logging](https://docs.python.org/3/library/logging.html) package.
