#!/bin/bash

# install the bluesky framework into an ipython profile

# usage: ./install_startup.sh [startup_directory [station_name [mongodb_server_host]]]

# such as `.ipython/ipython profile_bluesky/startup`
export DEST=${1:-/tmp/profile}
# terse station/instrument name such as `9-ID-C` or `USAXS`
export STATION=${2:-station}
# FQDN of workstation running our mongodb
export MONGO_SERVER=${3:-localhost.localdomain}

echo "Startup directory: ${DEST}"
echo "Station: ${STATION}"
echo "MongoDB server: ${MONGO_SERVER}"

if [ ! -d ${DEST} ]; then
    echo "creating installation directory: ${DEST}"
    mkdir -p ${DEST}
fi

export ODIR=`pwd`
export TMPL=${ODIR}/startup.tgz

if [ -f "${TMPL}" ]; then
    echo "${TMPL} exists"
else
    echo "copy the startup template"
    pushd profile_bluesky && tar czf ${TMPL} startup && popd
fi

# install the startup template
pushd ${DEST} && tar xzf ${TMPL} && popd

# edit the startup template

_places+=" 00-instrument.py"
_places+=" instrument/framework/metadata.py"
# export _places
# echo "_places = ${_places}"
for fname in ${_places}
do
    # replace `INSTRUMENT` with ${STATION}
    CMD="sed -i s:'INSTRUMENT':'${STATION}':g ${DEST}/startup/${fname}" \
       && eval ${CMD}
    #    && echo ${CMD}
done

CMD="sed -i s:'localhost.localdomain':'${MONGO_SERVER}':g ${DEST}/startup/mongodb_config.yml"; ${CMD}
