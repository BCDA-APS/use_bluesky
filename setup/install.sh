#!/bin/bash

# install the Components for BlueSky, Ophyd, and related NSLS-II DAQ

BLUESKY_ROOT=$HOME/Apps/BlueSky
SCRATCH_DIR=/tmp

#----------------------------------------------------
# Install Python via Miniconda installer
MINICONDA=$SCRATCH_DIR/miniconda.sh
wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O $MINICONDA
chmod +x $MINICONDA
mkdir -p $HOME/Apps
bash $MINICONDA -b -p ${BLUESKY_ROOT}
export PATH=${BLUESKY_ROOT}/bin:$PATH
conda update -y conda pip
python --version
conda --version
pip --version

#----------------------------------------------------
# add BlueSky and required packages
# ref: https://raw.githubusercontent.com/NSLS-II/tutorial/master/environment.yml

CONDA_CHANNELS=
CONDA_CHANNELS+=" -c conda-forge"
CONDA_CHANNELS+=" -c defaults"
CONDA_CHANNELS+=" -c soft-matter"
CONDA_CHANNELS+=" -c lightsource2-tag"

CONDA_PKGS=
CONDA_PKGS+=" metadatastore"

CONDA_PKGS+=" cython"
CONDA_PKGS+=" cytoolz"
CONDA_PKGS+=" git"
CONDA_PKGS+=" h5py"
CONDA_PKGS+=" ipython"
CONDA_PKGS+=" ipywidgets"
CONDA_PKGS+=" lxml"
CONDA_PKGS+=" matplotlib"
CONDA_PKGS+=" numpy"
CONDA_PKGS+=" pandas"
CONDA_PKGS+=" prettytable"
CONDA_PKGS+=" pymongo"
CONDA_PKGS+=" pyqt"
CONDA_PKGS+=" pytest"
CONDA_PKGS+=" pyyaml"
CONDA_PKGS+=" requests"
CONDA_PKGS+=" qt=4"
CONDA_PKGS+=" scikit-image"
CONDA_PKGS+=" scipy"
CONDA_PKGS+=" sympy"
CONDA_PKGS+=" tifffile"
CONDA_PKGS+=" ujson"

PIP_PKGS=
PIP_PKGS+=" boltons"
PIP_PKGS+=" mongoquery"
PIP_PKGS+=" pims"
PIP_PKGS+=" pyepics"
PIP_PKGS+=" pyRestTable"
PIP_PKGS+=" tzlocal"
PIP_PKGS+=" git+https://github.com/Nikea/historydict#egg=historydict"
PIP_PKGS+=" git+https://github.com/NSLS-II/amostra#egg=amostra"
PIP_PKGS+=" git+https://github.com/NSLS-II/bluesky#egg=bluesky"
PIP_PKGS+=" git+https://github.com/NSLS-II/databroker#egg=databroker"
PIP_PKGS+=" git+https://github.com/NSLS-II/doct#egg=doct"
PIP_PKGS+=" git+https://github.com/NSLS-II/event-model#egg=event_model"
PIP_PKGS+=" git+https://github.com/NSLS-II/filestore#egg=filestore"
PIP_PKGS+=" git+https://github.com/NSLS-II/filestore#egg=filestore"
#PIP_PKGS+=" git+https://github.com/NSLS-II/metadatastore#egg=metadatastore"
PIP_PKGS+=" git+https://github.com/NSLS-II/ophyd#egg=ophyd"
PIP_PKGS+=" git+https://github.com/NSLS-II/portable-fs#egg=portable_fs"
PIP_PKGS+=" git+https://github.com/NSLS-II/portable-mds#egg=portable_mds"
PIP_PKGS+=" git+https://github.com/NSLS-II/suitcase#egg=suitcase"

conda install -y $CONDA_CHANNELS   $CONDA_PKGS
pip install  $PIP_PKGS

#----------------------------------------------------
# PyEpics uses libCom which was built with libreadline
#  this conflicts with the one in miniconda
# Delete the libreadline from miniconda
# Some other packages depend on the conda install of the readline package.
# It won't uninstall cleanly.  Just remove it from the command line
# and hope the other packages can live with the libreadline installed in the OS.
#------
#use the Python "readline" package from conda and skip this delete
#/bin/rm -f ${BLUESKY_ROOT}/lib/libreadline*
