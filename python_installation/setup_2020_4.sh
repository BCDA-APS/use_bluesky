#!/bin/bash

# setup conda env for bluesky at an APS beam line or development host

export CONDA_ENVIRONMENT=bluesky_2020_4

# derived from: https://github.com/BCDA-APS/use_bluesky/wiki/Install-Bluesky-packages

# need a valid EPICS PV to test
export TEST_PV=""


# must activate a conda environment first

if [ -f "/APSshare/miniconda/x86_64/bin/activate" ]; then
    # Must be at APS
    # miniconda is faster than anaconda
    # it has fewer packages in base environment
    source /APSshare/miniconda/x86_64/bin/activate
    # APS Storage Ring Current
    export TEST_PV="'S:SRcurrentAI'"
elif [ -f "${HOME}/Apps/miniconda/bin/activate" ]; then
    source ${HOME}/Apps/miniconda/bin/activate
elif [ -f "${HOME}/Apps/anaconda/bin/activate" ]; then
    source ${HOME}/Apps/anaconda/bin/activate
else
    echo "Where is Anaconda activate?"
    exit 1
fi


existing=`conda env list | grep "${CONDA_ENVIRONMENT} "`
if [ "" != "${existing}" ]; then
    echo "conda env '${CONDA_ENVIRONMENT}' exists."
    echo "must remove it first: conda env remove -n ${CONDA_ENVIRONMENT}"
    exit 1
fi


echo "# environment ------------------------------"
# still conflicts for python 3.8, drop to 3.7
conda create -n ${CONDA_ENVIRONMENT} -y \
    python=3.7 ipython jupyter notebook pylint pymongo psutil h5py lxml

conda activate ${CONDA_ENVIRONMENT}


echo "# EPICS ------------------------------"
# epicscorelibs is EPICS 7.0.3 and it works.  Period.
conda install -y -c conda-forge epicscorelibs pyEpics
if [ "" != "${TEST_PV}" ]; then
    python -c "import epics; print(epics.caget(${TEST_PV}))"
fi


echo "# Bluesky framework ------------------------------"
conda install -y \
    -c defaults -c conda-forge -c nsls2forge -c aps-anl-tag -c pydm-tag \
    bluesky databroker event-model ophyd pygobject \
    apstools pyRestTable pvview spec2nexus stdlogpj \
    pydm imagecodecs-lite
if [ "" != "${TEST_PV}" ]; then
    python -c "import ophyd; pv= ophyd.EpicsSignal(${TEST_PV}, name='pv'); print(pv.value)"
fi

echo "# hklpy ------------------------------"
conda install hklpy -y -c lightsource2-tag
# if [ "" != "${TEST_PV}" ]; then
#     python -c "import ophyd; pv= ophyd.EpicsSignal(${TEST_PV}, name='pv'); print(pv.value)"
# fi


echo "# punx ------------------------------"
# punx: Python Utilities for NeXus
conda install -n ${CONDA_ENVIRONMENT} \
    -y PyGithub idna urllib3 requests deprecated pyjwt
pip install punx

echo ""
echo "conda env ${CONDA_ENVIRONMENT}'' created"
echo "activate with:  conda activate ${CONDA_ENVIRONMENT}"
