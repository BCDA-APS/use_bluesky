#!/bin/bash

# setup conda env for bluesky at an APS beam line or development host

export CONDA_ENVIRONMENT=bluesky_2020_4

# derived from: https://github.com/BCDA-APS/use_bluesky/wiki/Install-Bluesky-packages


# must activate a conda environment first
ACTIVATORS+=" /APSshare/miniconda/x86_64/bin/activate"
ACTIVATORS+=" ${HOME}/Apps/miniconda3/bin/activate"
ACTIVATORS+=" ${HOME}/Apps/Miniconda3/bin/activate"
ACTIVATORS+=" ${HOME}/Apps/miniconda/bin/activate"
ACTIVATORS+=" ${HOME}/Apps/Miniconda/bin/activate"
ACTIVATORS+=" ${HOME}/Apps/anaconda3/bin/activate"
ACTIVATORS+=" ${HOME}/Apps/Anaconda3/bin/activate"
ACTIVATORS+=" ${HOME}/Apps/anaconda/bin/activate"
ACTIVATORS+=" ${HOME}/Apps/Anaconda/bin/activate"
for d in ${ACTIVATORS}; do
    if [ -f "${d}" ]; then
        echo "${d} was found"
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
conda create -n ${CONDA_ENVIRONMENT} -y \
    python=3.7 ipython jupyter notebook pylint pymongo psutil h5py lxml

conda activate ${CONDA_ENVIRONMENT}


echo "#"
echo "# EPICS ------------------------------"
# epicscorelibs is EPICS 7.0.3 and it works.  Period.
conda install -y -c conda-forge epicscorelibs pyEpics


echo "#"
echo "# Bluesky framework ------------------------------"
conda install -y \
    -c defaults -c conda-forge -c nsls2forge -c aps-anl-tag -c pydm-tag \
    "bluesky>=1.6" "databroker>=1" event-model "ophyd>=1.4" pygobject \
    apstools pyRestTable pvview spec2nexus stdlogpj \
    pydm imagecodecs-lite


echo "#"
echo "# hklpy ------------------------------"
conda install -y hklpy -c lightsource2-tag


echo "#"
echo "# punx ------------------------------"
# punx: Python Utilities for NeXus
conda install -n ${CONDA_ENVIRONMENT} \
    -y PyGithub idna urllib3 requests deprecated pyjwt
pip install punx

echo "#"
echo "# conda env '${CONDA_ENVIRONMENT}' created"
echo "# activate with:    conda activate ${CONDA_ENVIRONMENT}"
