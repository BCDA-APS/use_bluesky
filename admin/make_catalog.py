#!/usr/bin/env python

"""
create a databroker catalog specification

Creates a configuration file used with mongoDB
to define a catalog used by databroker.

For usage, see:
https://github.com/BCDA-APS/use_bluesky/wiki/mongodb-server

Assumption: this program is run in the ~/.config/databroker directory.
"""

import os
import sys
import yaml

# TIME_ZONE = "America/Chicago"
TIME_ZONE = "US/Central"

def command_options():
    import argparse

    parser = argparse.ArgumentParser(
        prog=os.path.split(sys.argv[0])[-1],
        description=__doc__.strip().splitlines()[0],
        )

    parser.add_argument(
        'mongo_host',
        type=str,
        help="MongoDB server host name")

    parser.add_argument(
        'db_prefix',
        type=str,
        help="database prefix (e.g.: '45idc', no '.' allowed)")

    msg = (
            "use old-style Broker configuration YAML,"
            " default will use intake style catalog"
        )
    parser.add_argument('-b', 'broker', type=str, help=msg)

    return parser.parse_args()


def build_config(host, prefix):
    config = {
        "description" : "heavyweight shared database",
        "metadatastore" : {
            "module" : "databroker.headersource.mongo",
            "class" : "MDS",
            "config" : {
                "host" : host,
                "port" : 27017,
                "database" : f"{prefix}-run_data",
                "timezone" : TIME_ZONE,
            },
        },
        "assets" : {
            "module" : "databroker.assets.mongo",
            "class" : "Registry",
            "config" : {
                "host" : host,
                "port" : 27017,
                "database" : f"{prefix}-file_refs",
            },
        },
    }
    return config


def one_time_setup(db_name):
    import databroker
    cat = databroker.catalog[db_name]
    try:
        from databroker.assets.utils import install_sentinels
        conf_dict = cat.v1._config["metadatastore"]["config"]
        install_sentinels(conf_dict, version=1)
        print(f"{db_name}: installing version sentinels")
    except RuntimeError:
        print(f"{db_name}: version sentinels already installed")
    return len(cat)


def main():
    args = command_options()
    fname = f"{args.db_prefix}.yml"

    if os.path.exists(fname):
        print(f"file '{fname}' exists, will not overwrite.")
    else:
        config = build_config(args.mongo_host, args.db_prefix)
        with open(fname, "w") as fp:
            fp.write(yaml.dump(config))
        print(f"wrote: {fname}")

    count = one_time_setup(args.db_prefix)
    print(f"runs in the catalog: {count}")


if __name__ == "__main__":
    main()
