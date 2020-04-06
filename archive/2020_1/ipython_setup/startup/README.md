# ipython profile startup

This is the IPython startup directory when using mongodb with RW

.py and .ipy files in this directory will be run *prior* to any code or 
files specified via the exec_lines or exec_files configurables whenever 
you load this profile.

Files will be run in lexicographical order, so you can control the 
execution order of files with a prefix, e.g.::

    00-first.py
    50-middle.py
    99-last.ipy

BlueSky conventions:

    00   startup
    01   databroker
    10   motors
    20   detectors
    25   areadetector
    40   devices
    50   scans
    60   metadata

Note: 

* "-" sorts *before* numbers
* numbers sort *before* letters
* upper case sorts *before* lower case
* "_" sorts *after* letters
