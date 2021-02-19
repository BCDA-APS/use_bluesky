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
DB_PREFIX = "bs--"
SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR
WEEK = 7 * DAY

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


def ts2isotime(ts):
    """Convert Python timestamp float to ISO-8601 text."""
    return (
        datetime.datetime
        .fromtimestamp(ts)
        .isoformat(sep=" ", timespec="minutes")
    ).split()[0]


class Repositories:
    """
    Bluesky (databroker) data repositories by server.
    """

    def __init__(self, servers) -> None:
        if not isinstance(servers, list):
            servers = [servers]
        self.registry = {}
        self.since = ts2isotime(time.time() - 26 * WEEK)
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

    def _build_test_catalog(self):
        path = databroker.catalog_search_path()[0]
        config_file = os.path.join(path, "db_activity.yml")

        reg = {
            f"{DB_PREFIX}{repo}": dict(
                args=dict(
                    metadatastore_db = f"{server.uri}{pair.runs}",
                    asset_registry_db = f"{server.uri}{pair.refs}"
                ),
                driver="bluesky-mongo-normalized-catalog"
            )
            for host, server in self.registry.items()
            for repo, pair in server.repositories.items()
        }
        out = yaml.dump(dict(sources=reg))
        with open(config_file, "w") as f:
            f.write(out)

        return config_file

    def activity_report(self):
        config_file = self._build_test_catalog()
        table = pyRestTable.Table()
        table.addLabel("Mongodb server")
        table.addLabel("Databroker repository")
        table.addLabel("total runs")
        table.addLabel(f"runs since {self.since}")
        table.addLabel("first run")
        table.addLabel("last run")

        # Empirical:  Needed to add a pause here.
        # Without the pause, the YAML config we just wrote is not found.
        # 0.5 s was too short, 1 s worked.
        time.sleep(1)

        cat_list = list(databroker.yaml_catalogs)
        for bs_repo in cat_list:
            if not bs_repo.startswith(DB_PREFIX):
                continue
            repo = bs_repo[len(DB_PREFIX):]
            # print(repo)

            cat = databroker.catalog[bs_repo]
            host = cat._metadatastore_db.client.address[0]
            total_runs = len(cat)

            if total_runs:
                first_run = cat[-total_runs]
                last_run = cat[-1]
                first_date = ts2isotime(first_run.metadata["start"]["time"])
                last_date = ts2isotime(last_run.metadata["start"]["time"])
            else:
                first_date, last_date = "", ""

            search_period = databroker.queries.TimeRange(
                since=self.since,
                # until=until
            )

            recent_cat = cat.search(search_period)
            recent_runs = len(recent_cat)

            # fmt: off
            table.addRow(
                (
                    host,
                    repo,
                    total_runs,
                    recent_runs,
                    first_date,
                    last_date,
                )
            )
            # fmt: on

        os.remove(config_file)
        return table


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
    servers = """
        localhost
        32idcws
        arcturus
        bach
        eggplant
        groggy
        otz
        s100apps
        s8idapps
        usaxsserver
        wow
        xmd34id
    """
    repos = Repositories(servers)
    print("Bluesky (databroker) Repository Report")
    print(repos.repository_report())
    title = "Databroker Mongodb Server Activity Report"
    print(f"{title}: {ts2isotime(time.time())}")
    print(repos.activity_report())


if __name__ == "__main__":
    main()
