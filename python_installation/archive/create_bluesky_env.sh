#!/bin/bash

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

cd /tmp
# download the files we'll need
wget https://raw.githubusercontent.com/BCDA-APS/use_bluesky/master/python_installation/requirements.txt
wget https://raw.githubusercontent.com/BCDA-APS/use_bluesky/master/python_installation/pinned
wget https://raw.githubusercontent.com/BCDA-APS/use_bluesky/master/python_installation/.condarc

# create & install (-y means accept and proceed without asking)
CHANNELS="-c defaults -c conda-forge -c nsls2forge -c aps-anl-tag -c pydm-tag"
conda create -n bluesky -y $CHANNELS --file=requirements.txt

# learn where the bluesky environment is stored
where_is_conda_env bluesky

# install additional configurations
cp pinned ${conda_env_dir}/conda-meta/
cp .condarc ${conda_env_dir}/

# Automatic User Interface Creation from Ophyd Devices
if [ "Linux x86_64" == "`uname -ms`" ]; then
    # do this AFTER pinned so conda will not update tornado
    echo "NOTE: system is linux-64, installing typhon"
    conda activate bluesky
    conda install -y -c pcds-tag typhon
fi
