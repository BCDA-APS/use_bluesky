#!/bin/bash

# file: install_startup.sh
# purpose:
#     install Bluesky IPython startup directory
#     with default instrument package into `pwd`
#     (within a IPython profile directory).

# assumes tarball is in same directory as this bash script
export STARTUP_TARBALL="$(realpath $(dirname $0))/2021_1_startup.tar.gz"
# TODO: needs URL from GitHub repo
export STARTUP_URL="TODO:"


function show_usage() {
    echo "usage: $0 BEAMLINE INSTRUMENT CATALOG"
}

function perform_installation_tasks() {
    path=$(basename $(realpath $(pwd)))
    if [[ "$(echo $path | cut -f 1 -d '_')" != "profile" ]]; then
        echo "Not an IPython profile directory: '${path}'"
        echo "No installation."
        return
    fi
    # Will only proceed if in IPython configuration directory
    # Name style: profile_ABCDEFG
    PROFILE=$(echo $path | cut -f 2 -d '_')
    IPATH=$(dirname $(realpath $(dirname ${path})))

    if [ -d "startup" ]; then
        echo "Existing 'startup'.  Will not modify."
        return
        # /bin/rm -rf ./startup
    fi

    if [ -f "${STARTUP_TARBALL}" ]; then
        echo "Extracting instrument package template: '${STARTUP_TARBALL}'"
        tar xzf ${STARTUP_TARBALL}
    else
        # TODO: If can't get the tarball locally, then need from URL
        # echo "Extracting instrument package template: '${STARTUP_URL}'"
        # wget ${STARTUP_URL} ./
        # tar xzf local_tarball_name
        # rm local_tarball_name
        return
    fi

    echo "Installing to IPython profile directory: '$(realpath ${path})'"
    BEAMLINE=$1
    INSTRUMENT=$2
    CATALOG=$3

    echo "setting beam line name: ${BEAMLINE}"
    sed -i s+"BEAMLINE_NAME"+"${BEAMLINE}"+g startup/README.md
    sed -i s+"BEAMLINE_NAME"+"${BEAMLINE}"+g startup/instrument/framework/metadata.py

    echo "setting instrument name: ${INSTRUMENT}"
    sed -i s+"INSTRUMENT_NAME"+"${INSTRUMENT}"+g startup/README.md
    sed -i s+"INSTRUMENT_NAME"+"${INSTRUMENT}"+g startup/instrument/framework/metadata.py

    echo "setting databroker catalog: ${CATALOG}"
    sed -i s+"CATALOG_NAME"+"${CATALOG}"+g startup/instrument/framework/initialize.py

    # edit starter script
    echo "editing starter shell script: $(realpath startup/blueskyStarter.sh)"
    echo "IPython directory: ${IPATH}"
    sed -i s+"IPYTHONDIR=~/.ipython-bluesky"+"IPYTHONDIR=${IPATH}"+g startup/blueskyStarter.sh
    echo "IPython profile: ${PROFILE}"
    sed -i s+"IPYTHON_PROFILE=bluesky"+"IPYTHON_PROFILE=${PROFILE}"+g startup/blueskyStarter.sh
}

if (( $# == 3 )); then
    perform_installation_tasks $1 $2 $3
else
    show_usage
fi
