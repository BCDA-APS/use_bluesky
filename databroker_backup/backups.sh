#!/bin/bash

# backup all the beamline mongodb servers for Bluesky

# example:  ./backups.sh 2>&1 | tee log_20190226-1406.txt

# server list: https://github.com/BCDA-APS/use_bluesky/wiki
# instructions: https://github.com/BCDA-APS/use_bluesky/blob/master/databroker_backup

export DUMPS_ROOT=/local/mongo-dumps

function do_backup
{
  echo "Bluesky databroker backup of ${1}"
  outdir=${DUMPS_ROOT}/${1}/
  mkdir -p ${outdir}
  mongodump --gzip --host ${2} --db metadatastore-production-v1 --out ${outdir}
  mongodump --gzip --host ${2} --db filestore-production-v1     --out ${outdir}
}

do_backup bcda   otz
do_backup 2bm    arcturus
do_backup 3id    dy
do_backup 9id    usaxsserver
do_backup 12idb  eggplant
do_backup 29id   groggy
do_backup 32id   32idcws
