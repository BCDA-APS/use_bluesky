print(__file__)
# set up the data broker (db) and make the RunEngine instance

import os

# load config from ~/.config/databroker/mongodb_config.yml
from databroker import Broker
db = Broker.named("mongodb_config")

RE = bluesky.RunEngine()
