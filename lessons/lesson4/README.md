# Lesson 4

In this lesson, a motor and noisy detector are simulated
using capabilities provided by 
the [ophyd](https://blueskyproject.io/ophyd/) package.

The noisy detector is configured to describe a narrow
Gaussian peak based on the value of the motor position.
The peak is centered somewhere between motor values -1 and +1.

## Objective

Use bluesky scans to find the peak center and width.
Move the motor to the peak center.

* [lesson4](lesson.ipynb) - find a peak and lineup on it


## Advanced

* Convert the interactive commands to a bluesky plan
  and run that plan to find the peak center.
* Add that new plan to the instrument package, then 
  restart the notebook's kernel and try it.
* Add the simulated motor and noisy detector to the 
  instrument package, then restart the notebook's 
  kernel and find the peak again.

## About ...

The instrument package included with this lesson is 
a brief version of the standard package used with any 
APS instrument.  Since the notebook is for teaching,
it does not connect with any mongodb 
database which means the scans are not kept by the
databroker.  However, every scan is saved to a 
SPEC data file as described when the instrument package
is loaded.
