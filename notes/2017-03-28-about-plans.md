# Overview: What is a BlueSky *plan*?

In [BlueSky](https://github.com/NSLS-II/bluesky), all activity happens by the execution of a *plan*.
A *plan* is a Python function that calls a sequence of *messages* which
constitute data acquisition operations 
such as a scan or even the collection of a single value, such as counting from a scaler.

**summary**: 

* *plan* : Python command that executes a sequence of *messages*.
* *message* : instance of [`bluesky.utils.Msg`](https://github.com/NSLS-II/bluesky/blob/master/bluesky/utils.py#L23).

    Msg(command, obj, *args, **kwargs)

## The BlueSky *Run Engine*

To understand the BlueSky *plan*, it is first necessary to understand in what context
a plan is used.

The *RunEngine* is a state machine (states: idle, running, paused), 
reponsible for executing a *plan*.  It will emit a series of *documents*
as it executes the plan.  *The Run Engine executes messages and emits Documents.*
(A *document* is the fundamental record of storage in the BlueSky datastore.  It is a 
[json](http://json.org/) string.)

These documents will take one of these forms:

* `start` : first document of a *plan*
* `descriptor`: -TODO- (? description of an event ?)
* `event` : one record of data of a *plan*, includes uid of *start* document
* `stop` : last document of a *plan*, includes uid of *start* document

A plan is *submitted* to the RunEngine through a call such as

    # setup
    from bluesky.global_state import gs
    RE = gs.RE  # convenience alias
    
    #
    RE(a_plan)

note: Specifically, we use `RE` as defined in 
[`bluesky.global_state`](https://github.com/NSLS-II/bluesky/blob/master/bluesky/global_state.py#L121)
as the single instance of the BlueSky *Run Engine*.  In fact, `RE` is an instance
of the `bluesky.global_state.RunEngineTraitType` class.  Use it as a 
[singleton](https://en.wikipedia.org/wiki/Singleton_pattern).

### Examples

Simplest example (from the 
[source code](https://github.com/NSLS-II/bluesky/blob/master/bluesky/run_engine.py#L488)):
    >>> RE(my_scan)

Examples using subscriptions (a.k.a. callbacks):

    >>> def print_data(doc):
    ...     print("Measured: %s" % doc['data'])
    ...
    >>> def celebrate(doc):
    ...     # Do nothing with the input.
    ...     print("The run is finished!!!")
    ...
    >>> RE(my_generator, subs={'event': print_data, 'stop': celebrate})

For every `event` documented emitted by the *Run Engine*, in addition
to anything else done by the *Run Engine*, `print_data()` will be called
and the method will print the contents of the `event` document.

### Definition of the call to `RE()`

[Briefly](https://github.com/NSLS-II/bluesky/blob/master/bluesky/run_engine.py#L488):

    RE(plan, subs=None, *, raise_if_interrupted=False, **metadata_kw)

## **Plan** Examples

## *Movable* & *Readable*

[*Movable* & *Readable*](https://github.com/NSLS-II/bluesky/blob/master/bluesky/run_engine.py#L488) 
are traits of detectors and positioners, respectively.

note:  There is reference to a *Flyable* but that is not defined in
[`bluesky.global_state`](https://github.com/NSLS-II/bluesky/blob/master/bluesky/global_state.py).
