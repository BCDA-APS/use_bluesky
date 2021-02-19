#!/usr/bin/env python

"""
Report the Bluesky run activity on given databroker servers.

Given a list of mongodb server host workstations,
inspect the various databases of each for Bluesky runs.
"""

from collections import namedtuple
import databroker
import databroker.queries
import datetime
import os
import pymongo
from pymongo.errors import ServerSelectionTimeoutError
import pyRestTable
import time
import yaml


DEFAULT_PORT = 27017

DatabaseNamePair = namedtuple("DatabaseNameSuffix", "runs refs")

# original database names
BROKER_DATABASE_NAMES = DatabaseNamePair(
    "metadatastore-production-v1", "filestore-production-v1"
)

DATABASE_NAME_SUFFIXES = [
    # 2020 database name suffixes
    DatabaseNamePair("run_data", "file_refs"),
    # 2021: same name for both metadata & assets
    # APS convention to add obvious "-bluesky" suffix
    DatabaseNamePair("bluesky", "__ignored__"),
    # developer testing
    DatabaseNamePair("headers", "assets"),
    DatabaseNamePair("metadata", "assets"),
    DatabaseNamePair("runs", "resources"),
]


class Repositories:
    """
    Bluesky (databroker) data repositories by server.
    """

    def __init__(self, servers) -> None:
        if not isinstance(servers, list):
            servers = [servers]
        self.registry = {}
        for server in servers:
            self.addServer(server)

    def addServer(self, host, port=DEFAULT_PORT):
        server = Server(host, port)
        self.registry[host] = server
        return server

    def repository_report(self):
        table = pyRestTable.Table()
        table.addLabel("host")
        table.addLabel("repository")
        table.addLabel("runs database")
        table.addLabel("file references db")
        for host, server in self.registry.items():
            for repo, pair in server.repositories.items():
                table.addRow((host, repo, pair.runs, pair.refs))
        return table

    def activity_report(self):
        path = databroker.catalog_search_path()[0]
        config_file = os.path.join(path, "db_activity.yml")
        # FIXME:from here
        with open(config_file, "w") as f:
            f.write(yaml.dump(dict(sources=registry)))

        table = pyRestTable.Table()
        table.addLabel("mongodb database")
        table.addLabel("server")
        table.addLabel(SEARCH_PERIOD_LABEL)
        table.addLabel("total runs")
        table.addLabel("first run")
        table.addLabel("last run")
        for instrument in registry.keys():
            if instrument in databroker.catalog:
                cat = databroker.catalog[instrument]
                server = cat._metadatastore_db.client.address[0]
                total_runs = len(cat)
                if total_runs:
                    first_run = cat[-total_runs]
                    last_run = cat[-1]
                    first_date = ts2isotime(first_run.metadata["start"]["time"])
                    last_date = ts2isotime(last_run.metadata["start"]["time"])
                else:
                    first_date, last_date = "", ""
                recent_cat = cat.search(SEARCH_PERIOD)
                recent_runs = len(recent_cat)
                table.addRow(
                    (
                        instrument[3:],
                        server,
                        recent_runs,
                        total_runs,
                        first_date,
                        last_date,
                    )
                )
        print(f"{TITLE}: {ts2isotime(time.time())}")
        print(table)
        os.remove(config_file)


class Server:
    """ A Mongodb server for databroker."""

    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.repositories = {}
        self.identifyRepositories()

    def get_databases(self):
        client = pymongo.MongoClient(self.uri)
        try:
            db_list = client.list_database_names()
        except ServerSelectionTimeoutError:
            return
        db_to_ignore = "admin config local".split()
        # fmt: off
        return [
            db_name
            for db_name in db_list
            if db_name not in db_to_ignore
        ]
        # fmt: on

    def identifyRepositories(self):
        db_list = self.get_databases()
        run_db, ref_db = BROKER_DATABASE_NAMES
        if run_db in db_list:
            # Original-style database names
            db_list.remove(run_db)
            if ref_db in db_list:
                db_list.remove(ref_db)
            else:
                ref_db = run_db
            repo = DatabaseNamePair(run_db, ref_db)
            self.repositories["production-v1"] = repo

        while len(db_list):
            db_name = db_list.pop()

            def _check_pattern(run_suffix, ref_suffix):
                if not db_name.endswith(run_suffix):
                    return
                run_db = db_name
                instrument = db_name[: -len(run_suffix)].rstrip("-")
                ref_db = f"{instrument}-{ref_suffix}"
                if ref_db in db_list:
                    db_list.remove(ref_db)
                else:
                    ref_db = ""
                return instrument, run_db, ref_db

            for pair in DATABASE_NAME_SUFFIXES:
                args = _check_pattern(pair.runs, pair.refs)
                if args is not None:
                    instrument, run_db, ref_db = args
                    repo = DatabaseNamePair(run_db, ref_db)
                    self.repositories[instrument] = repo
                    break

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    @property
    def uri(self):
        return f"mongodb://{self.host}:{self.port}/"


def main():
    repos = Repositories("localhost")
    print("Bluesky (databroker) Repository Report")
    print(repos.repository_report())


if __name__ == "__main__":
    main()
