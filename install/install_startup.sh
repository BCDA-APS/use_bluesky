#!/bin/bash

# file: install_startup.sh
# purpose:
#     install Bluesky IPython startup directory
#     with default instrument package into `pwd`
#     (within a IPython profile directory).
#
# EXAMPLE
#     cd ~/.ipython-bluesky/profile_bluesky
#     path/to/install_startup.sh 45ID WNI wnicat
#
# (base) jemian@wow ~/.ipython/profile_testing $ /home/beams/JEMIAN/Documents/projects/BCDA-APS/use_bluesky/install/install_startup.sh 45ID WNI wnicat
# Extracting instrument package template: '/home/beams1/JEMIAN/Documents/projects/BCDA-APS/use_bluesky/install/2021_1_startup.tar.gz'
# Installing to IPython profile directory: '/home/beams1/JEMIAN/.ipython/profile_testing/profile_testing'
# setting beam line name: 45ID
# setting instrument name: WNI
# setting databroker catalog: wnicat
# editing starter shell script: /home/beams1/JEMIAN/.ipython/profile_testing/startup/blueskyStarter.sh
# IPython directory: /home/beams1/JEMIAN/.ipython
# IPython profile: testing


# assumes tarball is in same directory as this bash script
export TARNAME=2021_1_startup.tar.gz
export STARTUP_TARBALL="$(realpath $(dirname $0))/${TARNAME}"
# or get from web site
export REPO=https://github.com/BCDA-APS/use_bluesky
export STARTUP_URL="${REPO}/raw/main/install/${TARNAME}"


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
        # If can't get the tarball locally, then get from URL
        echo "Extracting instrument package template: '${STARTUP_URL}'"
        wget ${STARTUP_URL} ./
        tar xzf ${TARNAME}
        rm ${TARNAME}
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
