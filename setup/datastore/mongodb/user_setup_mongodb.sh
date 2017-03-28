#!/bin/bash

# install mongodb setup for BlueSky DataBroker

WWW_REPO=https://raw.githubusercontent.com/BCDA-APS/use_bluesky/master/setup/datastore/mongodb

#----------------------------------------------------
# mongodb configuration for databroker
FILE_LIST=
FILE_LIST+=" filestore/connection.yml"
FILE_LIST+=" metadatastore/connection.yml"

TARGET=${HOME}/.config
mkdir -p ${TARGET}/filestore ${TARGET}/metadatastore
for filename in ${FILE_LIST}; do
	wget ${WWW_REPO}/${filename} -O ${TARGET}/${filename}
done
