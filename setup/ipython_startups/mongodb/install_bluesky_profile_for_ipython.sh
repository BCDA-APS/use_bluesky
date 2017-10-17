#!/bin/bash

# install ipython setup for BlueSky, Ophyd, and related NSLS-II DAQ

PROFILE=bluesky

# note: if this profile has not yet been created, will create

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
FILE_LIST+=" mongodb_config.yml"
FILE_LIST+=" README.md"

WWW_REPO=https://raw.githubusercontent.com/BCDA-APS/use_bluesky/master/setup/ipython_startups/mongodb
TARGET=${HOME}/.ipython/profile_$PROFILE
for filename in ${FILE_LIST}; do
	wget ${WWW_REPO}/${filename} -O ${TARGET}/startup/${filename}
done

mkdir -p ${HOME}/.config/databroker
cd ${HOME}/.config/databroker
ln -s ../../.ipython/profile_$PROFILE/startup/mongodb_config.yml ./
