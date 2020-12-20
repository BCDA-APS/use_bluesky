#!/bin/bash

# setup conda env for bluesky at an APS beam line or development host
#
# note:
#   this script can be run on linux and Windows using bash:
#
#   bash ./setup_2020_9.sh [CONDA_ENVIRONMENT [ACTIVATE]]
#
#   where:
#
#   =================  ==============================
#   OPTION             EXAMPLE
#   =================  ==============================
#   CONDA_ENVIRONMENT  bluesky_2020_9
#   ACTIVATE           /path/to/Anaconda/bin/activate
#   =================  ==============================

export VERS=2020_9
export CONDA_ENVIRONMENT=${1:-bluesky_${VERS}}
export ACTIVATE=${2:-/APSshare/miniconda/x86_64/bin/activate}

echo "CONDA_ENVIRONMENT: ${CONDA_ENVIRONMENT}"
echo "ACTIVATE: ${ACTIVATE}"

# must activate a conda environment first
ACTIVATORS+=" ${ACTIVATE}"
ACTIVATORS+=" ${HOME}/Apps/miniconda3/bin/activate"
ACTIVATORS+=" ${HOME}/Apps/Miniconda3/bin/activate"
ACTIVATORS+=" ${HOME}/Apps/miniconda/bin/activate"
ACTIVATORS+=" ${HOME}/Apps/Miniconda/bin/activate"
ACTIVATORS+=" ${HOME}/Apps/anaconda3/bin/activate"
ACTIVATORS+=" ${HOME}/Apps/Anaconda3/bin/activate"
ACTIVATORS+=" ${HOME}/Apps/anaconda/bin/activate"
ACTIVATORS+=" ${HOME}/Apps/Anaconda/bin/activate"
ACTIVATORS+=" ${HOME}/Apps/Anaconda3/Scripts/activate"
for d in ${ACTIVATORS}; do
    if [ -f "${d}" ]; then
        echo "found: ${d}"
        source ${d}
        ACTIVATED=${d}
        break
    fi
done
if [ "" == "${ACTIVATED}" ]; then
    echo "Could not activate a conda base environment."
    echo "Where is Miniconda or Anaconda installed?"
    exit 1
fi


existing=`conda env list | grep "${CONDA_ENVIRONMENT} "`
if [ "" != "${existing}" ]; then
    echo "conda env '${CONDA_ENVIRONMENT}' exists."
    echo "must remove it first: conda env remove -n ${CONDA_ENVIRONMENT}"
    exit 1
fi


echo "#"
echo "# environment ------------------------------"
# still conflicts for python 3.8, drop to 3.7
conda env create -n ${CONDA_ENVIRONMENT} -f environment_${VERS}.yml

conda activate ${CONDA_ENVIRONMENT}


echo "# ------------------------------"
echo "#"
echo "# conda env '${CONDA_ENVIRONMENT}' created"
echo "# activate with:    conda activate ${CONDA_ENVIRONMENT}"
