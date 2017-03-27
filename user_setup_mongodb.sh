#!/bin/bash

# install mongodb setup for BlueSky DataBroker

APS_GITLAB=https://git.aps.anl.gov/jemian/deployments/raw/master/BlueSky/mongo

#----------------------------------------------------
# mongodb configuration for databroker
FILE_LIST=
FILE_LIST+=" filestore/connection.yml"
FILE_LIST+=" metadatastore/connection.yml"

TARGET=${HOME}/.config
mkdir -p ${TARGET}/filestore ${TARGET}/metadatastore
for filename in ${FILE_LIST}; do
	wget ${APS_GITLAB}/${filename} -O ${TARGET}/${filename}
done
