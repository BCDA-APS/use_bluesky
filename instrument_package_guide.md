# Instrument Package Guide


**Contents**
- [Instrument Package Guide](#instrument-package-guide)
  - [Add Motor(s)](#add-motors)
  - [Add Scaler(s)](#add-scalers)
  - [Re-organize into Devices](#re-organize-into-devices)
  - [Add Area Detector(s)](#add-area-detectors)
  - [Other Device Support](#other-device-support)
  - [Implement Custom Plans](#implement-custom-plans)
  - [Review Metadata](#review-metadata)

## Add Motor(s)

TODO:
## Add Scaler(s)

TODO:
## Re-organize into Devices

TODO:
## Add Area Detector(s)

TODO:
## Other Device Support

TODO:
## Implement Custom Plans

TODO:

If you are translating PyEpics code to Bluesky plans, consult this
[guide](https://blueskyproject.io/bluesky/from-pyepics-to-bluesky.html?highlight=blocking).

Keep in mind that a plan should not call code that blocks execution of the bluesky
*RunEngine* from conducting its periodic background actions. One such example is
the [`sleep()`
action](https://blueskyproject.io/bluesky/tutorial.html?highlight=blocking)
sometimes used to control sequencing of events.  More discussion of _blocking_
is provided in the context of how the RunEngine processes its
[Messages](https://blueskyproject.io/bluesky/msg.html?highlight=blocking).

## Review Metadata

TODO:
