#!/bin/bash

export CONDA_ACTIVATE=${HOME}/Apps/anaconda/bin/activate
export CONDA_ENVIRONMENT=bluesky_2020_9
# bluesky

export IPYTHON_PROFILE=bluesky
export IPYTHONDIR=~/.ipython

export OPTIONS=""
export OPTIONS="${OPTIONS} --profile=${IPYTHON_PROFILE}"
export OPTIONS="${OPTIONS} --ipython-dir=${IPYTHONDIR}"
export OPTIONS="${OPTIONS} --IPCompleter.use_jedi=False"
export OPTIONS="${OPTIONS} --InteractiveShellApp.hide_initial_ns=False"

source ${CONDA_ACTIVATE} ${CONDA_ENVIRONMENT}
ipython ${OPTIONS}
