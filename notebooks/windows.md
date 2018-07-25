# Installing in Windows 10

* install anaconda python 3.6 or higher
* `conda install networkx `
* `conda install -c conda-forge historydict jsonschema toolz tqdm super_state_machine pyepics`
* clone these projects from GitHub:
  * https://github.com/NSLS-II/bluesky
  * https://github.com/NSLS-II/databroker
  * https://github.com/NSLS-II/event-model
  * https://github.com/NSLS-II/ophyd
* in top-level directory each of those projects: `pip install .`

For the databroker, you might want to have a mongodb server running on your LAN.  Install details not provided here.
