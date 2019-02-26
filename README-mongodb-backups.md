
# How to backup (and move/merge bluesky's mongodb data)

:ref:
    https://stackoverflow.com/a/7232492/1046449

## Goal

* Periodically, backup the mongodb data for any installation 
  with the goal of using that backup as loss prevention in case
  of corruption of the mongodb datastore.

* Secondary goal is to prepare the data for transfer to a new 
  mongodb server or, even possibly, to merge with a different,
  existing mongodb server.

## Background

There are some tools in databroker for this.
When testing them in 
[fall 2018](https://github.com/APS-3ID-IXN/ipython-s3blue/issues/2), 
the existing tools
raised exceptions with some of the data labels that had 
been pulled from EPIC scaler channel name strings.  Some 
of the names, albeit having been accepted by ophyd and 
passed through bluesky documents to the databroker were 
found to be unacceptable to the data transfer tools.

## Preparation for Backup

Change the working directory to a partition with sufficient size for
the anticipated backup.

Identify the names of the mongodb server and the two mongodb 
databases used by databroker.  This information is described in the
databroker configuration file, usually: 
`~BEAMLINE_USER/.config/databroker/mongodb_config.yml`

(On Windows, use `%HOME%\AppData\Roaming\databroker\mongodb_config.yml`)

The database names are usually `metadatastore-production-v1` 
and `filestore-production-v1`.

## Backup (using `mongodump`)

:docs:
	https://docs.mongodb.com/manual/reference/program/mongodump/

For any databroker installation, there are two databases to backup:
`metadatastore-production-v1` and `filestore-production-v1`.

Backup mongodb with these steps::

   cd $DIRECTORY_WITH_MONGODB_DUMP_SUBDIRECTORIES
   mongodump --gzip  --db metadatastore-production-v1 
   mongodump --gzip  --db filestore-production-v1     

This will create directories `dump/metadatastore-production-v1/` and
`dump/filestore-production-v1/` and fill each with the backups.  Note
that the `--gzip  ` option is only available with mongodump and 
mongorestore since v3.2.

## Restore (using `mongorestore`)

:ref:
    https://stackoverflow.com/a/7232492/1046449

:docs:
	https://docs.mongodb.com/manual/reference/program/mongorestore/

Restore (and merge any non-duplicate documents, duplicates will be 
ignored) with these steps::

   cd $DIRECTORY_WITH_MONGODB_DUMP_SUBDIRECTORIES
   mongorestore --db metadatastore-production-v1 dump/metadatastore-production-v1/
   mongorestore --db filestore-production-v1     dump/filestore-production-v1/

