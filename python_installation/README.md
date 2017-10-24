# Install NSLS-II BlueSky into Linux x86_64

## Alternative

See these instructions instead. 
They include installation of the various requirements.

* https://git.aps.anl.gov/jemian/deployments/blob/master/BlueSky/install.sh


## download Miniconda for Python3

    wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh

## install it

    bash Miniconda3-latest-Linux-x86_64.sh -b -p ~/Apps/bluesky
    export PATH=$HOME/Apps/bluesky/bin:$PATH
    conda update conda
    conda install  -y pyyaml git

## If using virtual environments

Use this file when creating & installing into an environment:
https://github.com/NSLS-II/tutorial/blob/master/environment.yml

That set of install files also needs:

    pip install -y pyepics

## Next questions

* How about a conda install requirements file?
* How to build such a thing? (https://conda.io/docs/using/envs.html#export-the-environment-file)
* How to use it?

## Note

Dan Allan notes:

We currently pin conda versions to:

    conda 4.0.5
    conda-env 2.4.5
    anaconda-client 1.4.0
    conda-build 1.19.0

I think just the first two are important, but that's the complete set. We would like to update to more modern versions, but for now that's the set that we are sure works.
