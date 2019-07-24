#!/bin/bash

# create conda environments for python2.7 and 3.7

OPTS=""
OPTS="${OPTS} -c aps-anl-tag"
OPTS="ipython"
OPTS="${OPTS} jupyter"
OPTS="${OPTS} matplotlib"
OPTS="${OPTS} h5py"
OPTS="${OPTS} numpy"
OPTS="${OPTS} scipy"
OPTS="${OPTS} sphinx"
OPTS="${OPTS} sphinx_rtd_theme"
OPTS="${OPTS} qt"
OPTS="${OPTS} pyqt"
OPTS="${OPTS} lxml"
OPTS="${OPTS} pymongo"
OPTS="${OPTS} pyepics"
OPTS="${OPTS} pandas"
OPTS="${OPTS} notebook"
OPTS="${OPTS} spec2nexus"
OPTS="${OPTS} pyRestTable"
OPTS="${OPTS} coverage"
OPTS="${OPTS} coveralls"
OPTS="${OPTS} conda-build"
OPTS="${OPTS} anaconda"
export OPTS
conda create -n py27 -y python=2.7 ${OPTS}
conda create -n py37 -y python=3.7 ${OPTS}
