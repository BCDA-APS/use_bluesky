#!/bin/bash

# create conda environments for python2.7 and 3.7

export APS_CHANNEL=aps-anl-tag
OPTS=""
OPTS="${OPTS} ipython"
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
OPTS="${OPTS} -c ${APS_CHANNEL}"
export OPTS

conda create -n py27 -y python=2.7 ${OPTS}
conda create -n py37 -y python=3.7 ${OPTS}

where_is_conda_env() {
	local envo sentence match stringarray
	
	envo="$1"
	match="^${envo} "
	sentence=`conda env list | grep "${match}"`

	if [ "" == "${sentence}" ]; then
	    echo "Could not find conda env: ${envo}"
	    conda_env_dir=""
	    return
	fi

	# technique thanks to:
	# https://stackoverflow.com/questions/1469849/how-to-split-one-string-into-multiple-strings-separated-by-at-least-one-space-in#13402368
	stringarray=($sentence)
	conda_env_dir=${stringarray[-1]}
}

# learn where the py27 environment is stored
where_is_conda_env py27

# install additional configurations
echo "python<3" > ${conda_env_dir}/conda-meta/pinned
/bin/cat <<EOM >${conda_env_dir}/.condarc
channels:
  - defaults
  - conda-forge
  - ${APS_CHANNEL}
EOM

# learn where the py37 environment is stored
where_is_conda_env py37

# install additional configurations
echo "python<4" > ${conda_env_dir}/conda-meta/pinned
/bin/cat <<EOM >${conda_env_dir}/.condarc
channels:
  - defaults
  - conda-forge
  - ${APS_CHANNEL}
EOM
