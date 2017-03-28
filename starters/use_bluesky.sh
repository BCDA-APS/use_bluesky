#!/bin/bash

# https://raw.githubusercontent.com/BCDA-APS/use_bluesky/master/starters/use_bluesky.sh

# start an interactive ipython session running BlueSky (from NSLS-II)
#
# usage:  use_bluesky.sh [profile_name]
#
#  Command Options
#     profile_name : name of existing ipython profile to use (default: $BLUESKY_PROFILE)
#
#  Environment Variable(s) (these are optional)
#     BLUESKY_BIN_DIR : absolute path to directory containing Python with BlueSky installed
#
#     The use_bluesky.sh script has default values for the environment variable(s).
#     BLUESKY_BIN_DIR__INTERNAL_DEFAULT : (the first of these to be found, in order)
#                                         "~/Apps/BlueSky/bin"
#                                         or "/APSshare/anaconda3/BlueSky/bin"
#                                         or "." (the fallback default if none of those are found)
#     BLUESKY_PROFILE__INTERNAL_DEFAULT : "bluesky"
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# define the default path to the Python with BlueSky installed
export BLUESKY_BIN_DIR__INTERNAL_DEFAULT=.
if [ -d ~/Apps/BlueSky/bin ]; then
  export BLUESKY_BIN_DIR__INTERNAL_DEFAULT=~/Apps/BlueSky/bin
elif [ -d /APSshare/anaconda3/BlueSky/bin ]; then
  export BLUESKY_BIN_DIR__INTERNAL_DEFAULT=/APSshare/anaconda3/BlueSky/bin
fi


export BLUESKY_PROFILE__INTERNAL_DEFAULT=bluesky

# pick values to use, either from environment variables or defaults
export BLUESKY_BIN_DIR=${BLUESKY_BIN_DIR:-$BLUESKY_BIN_DIR__INTERNAL_DEFAULT}
export BLUESKY_PROFILE=${1:-$BLUESKY_PROFILE__INTERNAL_DEFAULT}

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

export PATH=$BLUESKY_BIN_DIR:$PATH
echo "starting ipython with profile: $BLUESKY_PROFILE"
which python
python --version
conda --version
pip --version
which ipython
ipython --profile=$BLUESKY_PROFILE
