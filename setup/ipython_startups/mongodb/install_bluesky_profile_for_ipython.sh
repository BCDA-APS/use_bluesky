#!/bin/bash

# install ipython setup for BlueSky, Ophyd, and related NSLS-II DAQ

PROFILE=bluesky

#----------------------------------------------------
# ipython startup configuration
#ipython profile create default
ipython profile create $PROFILE

FILE_LIST=
FILE_LIST+=" 00-0-check-python35-running.py"
FILE_LIST+=" 00-1-check-bluesky-installed.py"
FILE_LIST+=" 00-startup.py"
FILE_LIST+=" 01-databroker.py"
FILE_LIST+=" 02-pyepics.py"
FILE_LIST+=" 10-motors.py"
FILE_LIST+=" 20-detectors.py"
FILE_LIST+=" 60-metadata.py"
FILE_LIST+=" 95_write_NeXus_when_stop.py"
FILE_LIST+=" 99-describe_item.py"

WWW_REPO=https://raw.githubusercontent.com/BCDA-APS/use_bluesky/master/setup/ipython_startups/mongodb
TARGET=${HOME}/.ipython/profile_$PROFILE
for filename in ${FILE_LIST}; do
	wget ${WWW_REPO}/ipython-startup/${filename} -O ${TARGET}/startup/${filename}
done
