#!/bin/bash

# setup conda env for bluesky at an APS beam line

# derived from: https://github.com/BCDA-APS/use_bluesky/wiki/Install-Bluesky-packages

# miniconda is faster than anaconda
# it has fewer packages in base environment
source /APSshare/miniconda/x86_64/bin/activate

export CONDA_ENVIRONMENT=bluesky_2020_1

# APS Storage Ring Current
export TEST_PV="'S:SRcurrentAI'"


# note: problems when using python 3.8, drop to 3.7 for now
conda create -n ${CONDA_ENVIRONMENT} -y \
    python=3.7 ipython jupyter pylint pymongo psutil

conda activate ${CONDA_ENVIRONMENT}


# epicscorelibs is EPICS 7.0.3 and it works.  Period.
conda install -y -c conda-forge epicscorelibs pyEpics
python -c "import epics; print(epics.caget(${TEST_PV}))"


conda install -y \
    -c defaults -c conda-forge -c nsls2forge -c aps-anl-tag -c pydm-tag \
    bluesky databroker event-model ophyd pygobject \
    apstools pyRestTable pvview spec2nexus stdlogpj \
    pydm \
    imagecodecs-lite
# FIXME: conda install hklpy -y -c lightsource2-tag
# Diffractometer support configuration needs attention,
# not working now.
python -c "import ophyd; pv= ophyd.EpicsSignal(${TEST_PV}, name='pv'); print(pv.value)"


# ophyd 1.4.0rc4 has configurable timeout patch, use 10 s
pip install ophyd==1.4.0rc4
python -c "import ophyd; pv= ophyd.EpicsSignal(${TEST_PV}, name='pv'); print(pv.value)"

# bluesky 1.6.0rc4 because ___________________ (?)
pip install bluesky==1.6.0rc4
# TODO: python -c "import gi; gi.require_version('Hkl', '5.0'); from hkl.diffract import E6C"

# incompatibilities installing apstools >1.1.16 from conda or pip
# install most recent release on PyPI, ignoring dependencies
pip install -U apstools --no-deps
