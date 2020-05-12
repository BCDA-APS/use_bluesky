## Install NSLS-II Bluesky into Windows x86_64

* caution: (2020-05-12) These notes should be updated for the 2020_5 setup.  I ran that bash script *once* in Windows and it sort of worked with some help.  Needs to be documented properly.
* caution: These are my installation notes, not yet a complete set of instructions for others.

### Install mongodb

* https://www.mongodb.com/download-center/community
* Looks like an easy install

### Setup custom conda virtual environment

Assume Anaconda python distribution is already installed.
We'll add a conda virtual environment for bluesky.

1. start the powershell
1. switch to `cmd.exe`

note: test this with a Windows bash shell or work it up as a Windows batch file

```
CONDA_CHANNELS=
CONDA_CHANNELS+=" -c lightsource2-tag"
CONDA_CHANNELS+=" -c conda-forge"
CONDA_CHANNELS+=" -c defaults"
CONDA_CHANNELS+=" -c soft-matter"

CONDA_PKGS=
CONDA_PKGS+=" python=3"
CONDA_PKGS+=" cython"
CONDA_PKGS+=" cytoolz"
CONDA_PKGS+=" epics-base"
CONDA_PKGS+=" git"
CONDA_PKGS+=" h5py"
CONDA_PKGS+=" ipython"
CONDA_PKGS+=" ipywidgets"
CONDA_PKGS+=" lxml"
CONDA_PKGS+=" matplotlib"
CONDA_PKGS+=" networkx"
CONDA_PKGS+=" numpy"
CONDA_PKGS+=" pandas"
CONDA_PKGS+=" prettytable"
CONDA_PKGS+=" pycairo"
CONDA_PKGS+=" pyepics"
CONDA_PKGS+=" pymongo"
CONDA_PKGS+=" pyqt"
CONDA_PKGS+=" pytest"
CONDA_PKGS+=" pyyaml"
CONDA_PKGS+=" requests"
CONDA_PKGS+=" qt"
CONDA_PKGS+=" scikit-image"
CONDA_PKGS+=" scipy"
CONDA_PKGS+=" sympy"
CONDA_PKGS+=" tifffile"
# should pin tornado to v4
CONDA_PKGS+=" tornado=4"
CONDA_PKGS+=" ujson"

PIP_PKGS=
PIP_PKGS+=" boltons"
PIP_PKGS+=" mongoquery"
PIP_PKGS+=" pims"
# PIP_PKGS+=" pyepics"
PIP_PKGS+=" pyRestTable"
PIP_PKGS+=" tzlocal"
PIP_PKGS+=" pygobject3"

PIP_PKGS+=" git+https://github.com/Nikea/historydict#egg=historydict"
PIP_PKGS+=" git+https://github.com/NSLS-II/amostra#egg=amostra"
PIP_PKGS+=" git+https://github.com/NSLS-II/bluesky#egg=bluesky"
PIP_PKGS+=" git+https://github.com/NSLS-II/databroker#egg=databroker"
PIP_PKGS+=" git+https://github.com/NSLS-II/doct#egg=doct"
PIP_PKGS+=" git+https://github.com/NSLS-II/event-model#egg=event_model"
PIP_PKGS+=" git+https://github.com/NSLS-II/ophyd#egg=ophyd"
PIP_PKGS+=" git+https://github.com/NSLS-II/suitcase#egg=suitcase"
PIP_PKGS+=" git+https://github.com/NSLS-II/hklpy#egg=hklpy"

conda create -n bluesky -y $CONDA_CHANNELS   $CONDA_PKGS
activate bluesky
# conda install -y $CONDA_CHANNELS   $CONDA_PKGS
pip install $PIP_PKGS

# conda install -c lightsource2-tag -c conda-forge -c defaults -c soft-matter  cython  cytoolz git h5py ipython ipywidgets lxml matplotlib numpy pandas prettytable pyepics pymongo pyqt pytest pyyaml requests scikit-image scipy sympy  tifffile ujson

```

### prevent `tornado` from updating

For now, we need to [*pin*](https://conda.io/docs/user-guide/tasks/manage-pkgs.html#preventing-packages-from-updating-pinning) 
the installed tornado package to v4 so it
will not be updated to v5 or greater.  

1. Locate the directory for this conda environment.
   For me, `C:\Users\Pete\Apps\Anaconda\envs\bluesky`.
1. Open the `conda-meta` directory
1. Create a file named `pinned`
1. open that file in an editor and add this content:

    tornado<5

### Ipython directory

`C:\Users\Pete\.ipython\profile_default\startup`
