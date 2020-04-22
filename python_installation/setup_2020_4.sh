#!/bin/bash

# setup conda env for bluesky at an APS beam line

# derived from: https://github.com/BCDA-APS/use_bluesky/wiki/Install-Bluesky-packages

# need a valid EPICS PV to test
export TEST_PV=""

# miniconda is faster than anaconda
# it has fewer packages in base environment
if [ -d "/APSshare/miniconda/x86_64/bin" ]; then
    source /APSshare/miniconda/x86_64/bin/activate
    # APS Storage Ring Current
    export TEST_PV="'S:SRcurrentAI'"
elif [ -d "${HOME}/Apps/miniconda/bin/activate" ]; then
    source ${HOME}/Apps/miniconda/bin/activate
elif [ -d "${HOME}/Apps/anaconda/bin/activate" ]; then
    source ${HOME}/Apps/anaconda/bin/activate
else
    echo "Where is Anaconda activate?"
    exit 1
fi


export CONDA_ENVIRONMENT=bluesky_2020_4

existing = `conda env list | grep "${CONDA_ENVIRONMENT} "`
if [ "" != "${existing}" } ]; then
    echo "conda env '${existing}' exists."
    echo "must remove it first: conda env rm ${existing}"
    exit 1
fi


conda create -n ${CONDA_ENVIRONMENT} -y \
    python ipython jupyter pylint pymongo psutil h5py

conda activate ${CONDA_ENVIRONMENT}


# epicscorelibs is EPICS 7.0.3 and it works.  Period.
conda install -y -c conda-forge epicscorelibs pyEpics
if [ "" != "${TEST_PV}" } ]; then
    python -c "import epics; print(epics.caget(${TEST_PV}))"
fi

conda install -y \
    -c defaults -c conda-forge -c nsls2forge -c aps-anl-tag -c pydm-tag \
    bluesky databroker event-model ophyd pygobject \
    apstools pyRestTable pvview spec2nexus stdlogpj \
    pydm \
    imagecodecs-lite
conda install hklpy -y -c lightsource2-tag
if [ "" != "${TEST_PV}" } ]; then
    python -c "import ophyd; pv= ophyd.EpicsSignal(${TEST_PV}, name='pv'); print(pv.value)"
fi
