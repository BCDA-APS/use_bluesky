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

    parser.add_argument(
        '-b',
        '--broker',
        default=False,
        action='store_true',
        help=(
            "use old-style Broker configuration YAML,"
            " default will use intake style catalog"
        ),
    )

    parser.add_argument(
        '-o',
        '--output_path',
        type=str,
        default=".",
        help=(
            "directory in which to write configuration"
            ", default is current directory"
        ),
    )

    return parser.parse_args()


def build_broker_config(host, prefix):
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


def build_intake_config(host, prefix):
    port = 27017
    preamble = f"mongodb://{host}:{port}/{prefix}"
    config = dict(
        sources={
            prefix: dict(
                args=dict(
                    metadatastore_db=f"{preamble}-run_data",
                    asset_registry_db=f"{preamble}-file_refs",
                ),
                driver="bluesky-mongo-normalized-catalog",
            )
        }
    )
    return config


def one_time_setup(args):
    import databroker

    db_name = args.db_prefix
    cat = databroker.catalog[db_name]
    if args.broker:
        try:
            from databroker.assets.utils import install_sentinels
            conf_dict = cat.v1._config["metadatastore"]["config"]
            install_sentinels(conf_dict, version=1)
            print(f"{db_name}: installing version sentinels")
        except RuntimeError:
            print(f"{db_name}: version sentinels already installed")
    return len(cat)


def setup(args):
    if not os.path.exists(args.output_path):
        raise FileNotFoundError(
            f"Output path '{args.output_path}' not found."
        )
    fname = os.path.abspath(
        os.path.join(args.output_path, f"{args.db_prefix}.yml")
    )

    if os.path.exists(fname):
        print(f"file '{fname}' exists, will not overwrite.")
    else:
        if args.broker:
            builder = build_broker_config
        else:
            builder = build_intake_config
        config = builder(args.mongo_host, args.db_prefix)
        with open(fname, "w") as fp:
            fp.write(yaml.dump(config))
        print(f"wrote: {fname}")

    count = one_time_setup(args)
    print(f"runs in the catalog: {count}")


def main():
    args = command_options()
    setup(args)


if __name__ == "__main__":
    main()
