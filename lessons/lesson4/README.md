# Lesson 4

In this lesson, a motor and noisy detector are simulated
using capabilities provided by 
the [ophyd](https://blueskyproject.io/ophyd/) package.

The noisy detector is configured to describe a narrow
Gaussian peak based on the value of the motor position.
The peak is centered somewhere between motor values -1 and +1.

Objective:

Use bluesky scans to find the peak center and width.
Move the motor to the peak center.

* [lesson4](lesson4.ipynb) - find a peak and lineup on it


Advanced:

Convert the interactive commands to a bluesky plan
and run that plan to find the peak center.
