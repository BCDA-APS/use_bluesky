#!/bin/bash

# install ipython setup for BlueSky, Ophyd, and related NSLS-II DAQ

PROFILE1=bluesky
PROFILE2=BS_jupyter

# note: if this profile has not yet been created, will create


COMMON_FILE_LIST=
COMMON_FILE_LIST+=" 00-0-checks.py"
COMMON_FILE_LIST+=" 01-databroker.py"
COMMON_FILE_LIST+=" 02-pyepics.py"
COMMON_FILE_LIST+=" 09-imports.py"
COMMON_FILE_LIST+=" 10-devices.py"
COMMON_FILE_LIST+=" 15-motors.py"
COMMON_FILE_LIST+=" 20-detectors.py"
COMMON_FILE_LIST+=" 21-signals.py"
COMMON_FILE_LIST+=" 25-areadetector.py"
COMMON_FILE_LIST+=" 50-plans.py"
COMMON_FILE_LIST+=" 60-metadata.py"
COMMON_FILE_LIST+=" 80-callbacks.py"
COMMON_FILE_LIST+=" mongodb_config.yml"
COMMON_FILE_LIST+=" README.md"

#----------------------------------------------------
# ipython startup configuration
#ipython profile create default
ipython profile create ${PROFILE1}

FILE_LIST="${COMMON_FILE_LIST} 00-startup.py"

WWW_REPO=https://raw.githubusercontent.com/BCDA-APS/use_bluesky
WWW_DIR=${WWW_REPO}/master/ipython_setup/startup

TARGET=${HOME}/.ipython/profile_${PROFILE1}
for filename in ${FILE_LIST}; do
	wget ${WWW_DIR}/${filename} -O ${TARGET}/startup/${filename}
done

#----------------------------------------------------
#jupyter startup configuration
ipython profile create ${PROFILE2}

FILE_LIST="${COMMON_FILE_LIST} 00-startup-jup.py"

TARGET=${HOME}/.ipython/profile_${PROFILE2}
for filename in ${FILE_LIST}; do
	wget ${WWW_DIR}/${filename} -O ${TARGET}/startup/${filename}
done

#----------------------------------------------------

mkdir -p ${HOME}/.config/databroker
cd ${HOME}/.config/databroker
ln -s ../../.ipython/profile_${PROFILE1}/startup/mongodb_config.yml ./
ln -s ../../.ipython/profile_${PROFILE2}/startup/mongodb_config.yml ./
