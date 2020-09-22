Four-circle Diffractometer Demonstration

Demonstrate a four-circle diffractometer using the *hkl* package.

**CONTENTS**

- [Setup](#setup)
  - [Preparation](#preparation)
  - [The diffractometer object](#the-diffractometer-object)
  - [Operating mode](#operating-mode)
  - [Wavelength](#wavelength)
  - [Sample](#sample)
  - [Orientation](#orientation)
  - [Reflections](#reflections)
  - [Forward Solutions](#forward-solutions)
  - [Constraints](#constraints)
- [Example](#example)

# Setup

## Preparation

After starting a bluesky console or notebook session,
import the python gobject-introspection package that
is **required** to load the *hkl* support library.
This step *must* happen before the *hkl* package is first imported.

```python
import gi
gi.require_version('Hkl', '5.0')
```

Next, import the desired diffractometer geometry from the
[*hklpy*](https://github.com/bluesky/hklpy) package.  We pick
`E4CV` (Eulerian 4-Circle with Vertical scattering geometry)
as is typical at synchrotron beam lines.

```python
from hkl.diffract import E4CV
from hkl.util import Lattice
```

Next, we get additional packages that we may use.

```python
from apstools.diffractometer import Constraint
from apstools.diffractometer import DiffractometerMixin

from bluesky import plans as bp
from bluesky import plan_stubs as bps

from ophyd import Component
from ophyd import PseudoSingle
from ophyd import SoftPositioner
```

## The diffractometer object

Define a 4-circle class for our example with simulated motors.
There are attributes for the reciprocal space axes `h`, `k`, & `l`
and for the real space axes: `phi`, `omega`, `chi`, & `tth`.

```python
class FourCircleDiffractometer(DiffractometerMixin, E4CV):
    h = Component(PseudoSingle, '',
        labels=("hkl", "fourc"), kind="hinted")
    k = Component(PseudoSingle, '',
        labels=("hkl", "fourc"), kind="hinted")
    l = Component(PseudoSingle, '',
        labels=("hkl", "fourc"), kind="hinted")

    omega = Component(SoftPositioner,
        labels=("motor", "fourc"), kind="hinted")
    chi =   Component(SoftPositioner,
        labels=("motor", "fourc"), kind="hinted")
    phi =   Component(SoftPositioner,
        labels=("motor", "fourc"), kind="hinted")
    tth =   Component(SoftPositioner,
        labels=("motor", "fourc"), kind="hinted")
```

<details>
<summary>use EPICS motors instead of simulators</summary>

To use EPICS motors (`ophyd.EpicsMotor`) instead
of the `ophyd.SoftPositioner` simulators, redefine the
`FourCircleDiffractometer` class (or define a new
class) as follows, substituting with the proper motor PVs.

```python
class FourCircleDiffractometer(DiffractometerMixin, E4CV):
    h = Component(PseudoSingle, '',
        labels=("hkl", "fourc"), kind="hinted")
    k = Component(PseudoSingle, '',
        labels=("hkl", "fourc"), kind="hinted")
    l = Component(PseudoSingle, '',
        labels=("hkl", "fourc"), kind="hinted")

    omega = Component(EpicsMotor, "ioc:m1",
        labels=("motor", "fourc"), kind="hinted")
    chi =   Component(EpicsMotor, "ioc:m2",
        labels=("motor", "fourc"), kind="hinted")
    phi =   Component(EpicsMotor, "ioc:m3",
        labels=("motor", "fourc"), kind="hinted")
    tth =   Component(EpicsMotor, "ioc:m4",
        labels=("motor", "fourc"), kind="hinted")
```

</details>



Create the diffractometer object:

```python
fourc = FourCircleDiffractometer('', name='fourc')
```

The `fourc.wh()` method provides a quick summary of
the diffractometer:

```ipython
In [86]: fourc.wh()
===================== =========
term                  value
===================== =========
diffractometer        fourc
mode                  bissector
wavelength (angstrom) 1.54
h                     0.0
k                     0.0
l                     0.0
omega                 None
chi                   None
phi                   None
tth                   None
===================== =========
```

Print the value of the `omega` axis:

```ipython
In [54]: print(fourc.omega)
SoftPositioner(name='fourc_omega', parent='fourc', settle_time=0.0, timeout=None, egu='', limits=(0, 0), source='computed')

In [55]: print(fourc.omega.position)
None
```

Since `omega` was just created (see `SoftPositioner` above), it has no
value yet.  Use the `%mov` magic to set its value:

```ipython
In [57]: %mov fourc.omega 0

In [58]: print(fourc.omega.position)
0
```

When a diffractometer object is first created, it comes pre-defined
with certain defaults:

* operating mode
* wavelength
* sample
* orientation matrix
* axis constraints

The sections below will cover each of these.

## Operating mode

The default operating mode is `bissector`.  This mode
constrains `tth` to equal `2*omega`.

```ipython
In [21]: fourc.calc.engine.mode
Out[21]: 'bissector'
```

Print the list of available operating modes:

```ipython
In [22]: print(fourc.engine.modes)
['bissector', 'constant_omega', 'constant_chi', 'constant_phi', 'double_diffraction', 'psi_constant']
```

Change to `constant_phi` mode:

```ipython
In [29]: fourc.calc.engine.mode = "constant_phi"

In [30]: fourc.calc.engine.mode
Out[30]: 'constant_phi'
```

Change it back:

```ipython
In [31]: fourc.calc.engine.mode = "bissector"

In [32]: fourc.calc.engine.mode
Out[32]: 'bissector'
```

## Wavelength

The default wavelength is `1.54` angstroms.

```ipython
In [23]: fourc.calc.wavelength
Out[23]: 1.54
```

Change the wavelength (use angstrom):

```python
fourc.calc.wavelength = 1.62751693358
```

**NOTE**:
Stick to wavelength, at least for now.
Do not specify X-ray photon energy.
For the *hkl* code, specify wavelength in angstrom.  While the
documentation may state wavelength in `nm`, use `angstrom` since
these units *must* match the units used for the lattice parameters.
Also, note that the (internal) calculation of X-ray energy assumes
the units were `nm` so its conversion between energy and wavelength
is off by a factor of 10.

## Sample

The default sample is named `main` and is a hypothetical cubic
lattice with 1.54 angstrom edges.

```ipython
In [33]: fourc.calc.sample
Out[33]:
HklSample(name='main', lattice=LatticeTuple(a=1.54, b=1.54, c=1.54, alpha=90.0, beta=90.0, gamma=90.0), ux=Parameter(name='None (internally: ux)', limits=(min=-180.0, max=180.0), value=0.0, fit=True, inverted=False, units='Degree'), uy=Parameter(name='None (internally: uy)', limits=(min=-180.0, max=180.0), value=0.0, fit=True, inverted=False, units='Degree'), uz=Parameter(name='None (internally: uz)', limits=(min=-180.0, max=180.0), value=0.0, fit=True, inverted=False, units='Degree'), U=array([[1., 0., 0.],
       [0., 1., 0.],
       [0., 0., 1.]]), UB=array([[ 4.07999046e+00, -2.49827363e-16, -2.49827363e-16],
       [ 0.00000000e+00,  4.07999046e+00, -2.49827363e-16],
       [ 0.00000000e+00,  0.00000000e+00,  4.07999046e+00]]), reflections=[])
```

The diffractometer support maintains a list of all defined samples
(`fourc.calc._samples`).  The `fourc.calc.sample` symbol points
to one of these.  Let's illustrate by creating a new
sample `orthorhombic`:

```python
fourc.calc.new_sample('orthorhombic',
    lattice=Lattice(
        a=1, b=2, c=3,
        alpha=90.0, beta=90.0, gamma=90.0))
```

Now, there are two samples defined.  The `fourc.calc.sample` symbol
points to the new one:

```ipython
In [49]: len(fourc.calc._samples)
Out[49]: 2

In [50]: print(fourc.calc.sample.name)
orthorhombic
```

Switch back to the `main` sample:

```ipython
In [51]: fourc.calc.sample = "main"

In [52]: print(fourc.calc.sample.name)
main
```

Let's work with this sample now:

```python
fourc.calc.new_sample('EuPtIn4_eh1_ver',
    lattice=Lattice(
        a=4.542, b=16.955, c=7.389,
        alpha=90.0, beta=90.0, gamma=90.0))
```

## Orientation

This is the orientation matrix defined by default:

```ipython
In [74]: fourc.calc.sample.U
Out[74]:
array([[1., 0., 0.],
       [0., 1., 0.],
       [0., 0., 1.]])

In [75]: fourc.calc.sample.UB
Out[75]:
array([[ 4.07999046e+00, -2.49827363e-16, -2.49827363e-16],
       [ 0.00000000e+00,  4.07999046e+00, -2.49827363e-16],
       [ 0.00000000e+00,  0.00000000e+00,  4.07999046e+00]])
```

Change it by providing a new 3x3 array:

```ipython
In [80]: fourc.calc.sample.U = [[0, 1, 0], [0,0,1], [1,0,0]]

In [81]: fourc.calc.sample.U
Out[81]:
array([[0., 1., 0.],
       [0., 0., 1.],
       [1., 0., 0.]])
```
Set it back:

```ipython
In [82]: fourc.calc.sample.U = [[1,0,0], [0, 1, 0], [0,0,1]]
```

Similar for the *UB* matrix (`fourc.calc.sample.UB`).

## Reflections

A reflection associates a set of reciprocal-space axes (*hkl*) with
a set of real-space motor positions.  Two reflections are used
to calculate an orientation matix (UB matrix) which is used to
convert between motor positions and *hkl* values.

There are no reflections defined by default.

Define a reflection by associating a known *hkl* reflection
with a set of motor positions.

```python
position = fourc.calc.Position(
        omega=22.31594, chi=89.1377, phi=0, tth=45.15857)
r1 = fourc.calc.sample.add_reflection(0, 8, 0, position=position)
```

Define a second reflection (that is not a multiple
of the first reflection):

```python
r2 = fourc.calc.sample.add_reflection(
    0, 12, 1,
    position=fourc.calc.Position(
        omega=34.96232, chi=78.3139, phi=0, tth=71.8007))
```

Calculate the *UB* matrix from these two reflections:

```python
fourc.calc.sample.compute_UB(r1, r2)
```

## Forward Solutions

Forward solutions are the calculated combinations of real-space motor
positions given the sample oreitnation matrix,
reciprocal-space axes, operating mode,
wavelength, and applied constraints.  These combinations
are presented as a python list which may be empty if there are
no solutions.

The [`DiffractometerMixin`](https://apstools.readthedocs.io/en/latest/source/_diffractometer.html)
provides a helper to print the possible forward solutions for a
list of *hkl* reflections.  (Each reflection is provided as a
python tuple or list.)  Show just the first of the possible
solutions for each of the (100) and (010) reflections:

```ipython
In [97]: print(fourc.forwardSolutionsTable([[1,0,0],[0,1,0]]))
========= ======== ======== ======== ========= ========
(hkl)     solution omega    chi      phi       tth
========= ======== ======== ======== ========= ========
[1, 0, 0] 0        10.32101 0.20845  86.38310  20.64202
[0, 1, 0] 0        2.75098  89.09839 -16.98330 5.50196
========= ======== ======== ======== ========= ========
```

Show *all* the possible solutions by adding the `full=True` keyword:

```ipython
In [98]: print(fourc.forwardSolutionsTable([[1,0,0],[0,1,0]], full=True))
========= ======== ========== ========== ========= =========
(hkl)     solution omega      chi        phi       tth
========= ======== ========== ========== ========= =========
[1, 0, 0] 0        10.32101   0.20845    86.38310  20.64202
[1, 0, 0] 1        -10.32101  -0.20845   -93.61690 -20.64202
[1, 0, 0] 2        -169.67899 -0.20845   -93.61690 20.64202
[1, 0, 0] 3        -10.32101  -179.79155 86.38310  -20.64202
[1, 0, 0] 4        10.32101   179.79155  -93.61690 20.64202
[1, 0, 0] 5        -169.67899 -179.79155 86.38310  20.64202
[0, 1, 0] 0        2.75098    89.09839   -16.98330 5.50196
[0, 1, 0] 1        -2.75098   -90.90161  -16.98330 -5.50196
[0, 1, 0] 2        -2.75098   -89.09839  163.01670 -5.50196
[0, 1, 0] 3        2.75098    90.90161   163.01670 5.50196
[0, 1, 0] 4        -177.24902 -90.90161  -16.98330 5.50196
[0, 1, 0] 5        -177.24902 -89.09839  163.01670 5.50196
========= ======== ========== ========== ========= =========
```

For each of the reflections, six solutions were found possible.
The first solution is taken as the default.
A caller could access the complete list, such as:

```ipython
In [100]: fourc.calc.forward((1,0,0))
Out[100]:
(PosCalcE4CV(omega=10.321012278412818, chi=0.20844891265253537, phi=86.38309737706658, tth=20.642024556825636),
 PosCalcE4CV(omega=-10.321012278412818, chi=-0.20844891265253537, phi=-93.61690262293342, tth=-20.642024556825636),
 PosCalcE4CV(omega=-169.67898772158722, chi=-0.20844891265253537, phi=-93.61690262293342, tth=20.642024556825636),
 PosCalcE4CV(omega=-10.321012278412818, chi=-179.79155108734747, phi=86.38309737706658, tth=-20.642024556825636),
 PosCalcE4CV(omega=10.321012278412818, chi=179.79155108734747, phi=-93.61690262293342, tth=20.642024556825636),
 PosCalcE4CV(omega=-169.67898772158722, chi=-179.79155108734747, phi=86.38309737706658, tth=20.642024556825636))
```

and make a custom choice or constraints could be applied to
restrict the range of allowed solutions.

If there are no solutions to the forward calculation,
the *hkl* package raises a `ValueError` exception:

```
ValueError: Calculation failed (hkl-mode-auto-error-quark: none of the functions were solved !!! (0))
```

<details>
<summary>detailed exception trace</summary>

```ipython
In [114]: fourc.calc.forward((5, 4, 35))
---------------------------------------------------------------------------
Error                                     Traceback (most recent call last)
~/.conda/envs/bluesky_2020_9/lib/python3.8/site-packages/hkl/engine.py in pseudo_positions(self, values)
    212         try:
--> 213             geometry_list = self._engine.pseudo_axis_values_set(values,
    214                                                                 self._units)

Error: hkl-mode-auto-error-quark: none of the functions were solved !!! (0)

During handling of the above exception, another exception occurred:

ValueError                                Traceback (most recent call last)
<ipython-input-114-7b5743692787> in <module>
----> 1 fourc.calc.forward((5, 4, 35))

~/.conda/envs/bluesky_2020_9/lib/python3.8/site-packages/hkl/calc.py in wrapped(self, *args, **kwargs)
     42             initial_pos = self.physical_positions
     43             try:
---> 44                 return func(self, *args, **kwargs)
     45             finally:
     46                 self.physical_positions = initial_pos

~/.conda/envs/bluesky_2020_9/lib/python3.8/site-packages/hkl/calc.py in forward(self, position, engine)
    505                 raise ValueError('Engine unset')
    506
--> 507             self.engine.pseudo_positions = position
    508             return self.engine.solutions
    509

~/.conda/envs/bluesky_2020_9/lib/python3.8/site-packages/hkl/engine.py in pseudo_positions(self, values)
    214                                                                 self._units)
    215         except GLib.GError as ex:
--> 216             raise ValueError('Calculation failed (%s)' % ex)
    217
    218         Position = self._calc.Position

ValueError: Calculation failed (hkl-mode-auto-error-quark: none of the functions were solved !!! (0))
```

</details>

The `forwardSolutionsTable` does not raise an
error but displays `none` for that *hkl* reflection:

```ipython
In [121]: print(fourc.forwardSolutionsTable( [ [5,4,35], ], full=True))
========== ======== ===== === === ===
(hkl)      solution omega chi phi tth
========== ======== ===== === === ===
[5, 4, 35] none
========== ======== ===== === === ===
```

## Constraints

Constraints are applied to restrict the
motor positions that are allowed to be solutions of the forward
calculation from a reflection *hkl* to motor positions.

```
In [102]: fourc.showConstraints()
===== ========= ========== ===== ====
axis  low_limit high_limit value fit
===== ========= ========== ===== ====
omega -180.0    180.0      0.0   True
chi   -180.0    180.0      0.0   True
phi   -180.0    180.0      0.0   True
tth   -180.0    180.0      0.0   True
===== ========= ========== ===== ====
```

Apply a constraint that limits `phi >= 0`.  Create a dictionary
with the axis constraints to be applied.  The key is the axis name (must
be a name in the `fourc.calc.physical_axis_names` list).

```ipython
In [138]: fourc.calc.physical_axis_names
Out[138]: ['omega', 'chi', 'phi', 'tth']
```


The value is a
[`Constraint`](https://apstools.readthedocs.io/en/latest/source/_diffractometer.html) object.

`Constraint` Arguments

* low_limit (*number*) :
    Limit solutions for this axis to no less than `low_limit`.

* high_limit (*number*) :
    Limit solutions for this axis to no greater than `high_limit`.

* value (*number*) :
    When `fit=False`, calculate with axis = `value`.

* fit (*bool*) :
    When `True`, calculate new values for this axis.
    When `False`, keep this axis fixed at `value`.

```python
my_constraints = {
    # axis: Constraint(lo_limit, hi_limit, value, fit)
    "omega": Constraint(0, 180, 0, True),
    # "chi": Constraint(-180, 180, 0, True),
    # "phi": Constraint(-180, 180, 0, True),
    # "tth": Constraint(-180, 180, 0, True),
}
fourc.applyConstraints(my_constraints)
```

```ipython
In [109]: fourc.showConstraints()
===== ========= ========== ===== ====
axis  low_limit high_limit value fit
===== ========= ========== ===== ====
omega 0.0       180.0      0.0   True
chi   -180.0    180.0      0.0   True
phi   -180.0    180.0      0.0   True
tth   -180.0    180.0      0.0   True
===== ========= ========== ===== ====
```

Show all the possible solutions with these constraints:

```ipython
In [110]: print(fourc.forwardSolutionsTable([[1,0,0],[0,1,0]], full=True))
========= ======== ======== ========= ========= ========
(hkl)     solution omega    chi       phi       tth
========= ======== ======== ========= ========= ========
[1, 0, 0] 0        10.32101 0.20845   86.38310  20.64202
[1, 0, 0] 1        10.32101 179.79155 -93.61690 20.64202
[0, 1, 0] 0        2.75098  89.09839  -16.98330 5.50196
[0, 1, 0] 1        2.75098  90.90161  163.01670 5.50196
========= ======== ======== ========= ========= ========
```

Remove the constraint on `omega`:

```ipython
In [111]: fourc.undoLastConstraints()

In [112]: fourc.showConstraints()
===== ========= ========== ===== ====
axis  low_limit high_limit value fit
===== ========= ========== ===== ====
omega -180.0    180.0      0.0   True
chi   -180.0    180.0      0.0   True
phi   -180.0    180.0      0.0   True
tth   -180.0    180.0      0.0   True
===== ========= ========== ===== ====
```

# Example

We have some example information from a SPEC data file.
In summary, the sample and orientation information extracted is:

term | value(s)
--- | ---
sample | LNO_LAO
crystal |  3.781726143 3.791444574 3.79890313 90.2546203 90.01815424 89.89967858
geometry | fourc
mode | 0 (Omega equals zero)
lambda | 1.239424258
r1 | (0, 0, 2) 38.09875 19.1335 90.0135 0
r2 | (1, 1, 3) 65.644 32.82125 115.23625 48.1315
Q | (2, 2, 1.9) 67.78225 33.891 145.985 48.22875 -0.001 -0.16
UB[0] | -1.658712442     0.09820024135 -0.000389705578
UB[1] | -0.09554990312  -1.654278629    0.00242844486
UB[2] |  0.0002629818914 0.009815746824 1.653961812

**Note**: In SPEC's fourc geometry, the motors are reported
in this order: `tth omega chi phi`

1. use 4-circle geometry

    Reset all the above changes by re-creating the `fourc` object.

    ```python
    fourc = FourCircleDiffractometer('', name='fourc')
    ```

1. define the sample

    ```python
    fourc.calc.new_sample('LNO_LAO',
        lattice=Lattice(
            a=3.781726143, b=3.791444574 , c=3.79890313,
            alpha=90.2546203, beta=90.01815424, gamma=89.89967858))
    ```

1. set wavelength

    ```python
    fourc.calc.wavelength = 1.239424258
    ```

1. define two reflections

    ```python
    r1 = fourc.calc.sample.add_reflection(
        0, 0, 2,
        position=fourc.calc.Position(
            omega=19.1335, chi=90.0135, phi=0, tth=38.09875))
    r2 = fourc.calc.sample.add_reflection(
        1, 1, 3,
        position=fourc.calc.Position(
            omega=32.82125, chi=115.23625, phi=48.1315, tth=65.644))
    ```

1. calculate *UB* matrix

    ```ipython
    In [155]: fourc.calc.sample.compute_UB(r1, r2)
        ...: fourc.calc.sample.UB
        ...:
    Out[155]:
    array([[-9.55499011e-02, -1.65427863e+00,  2.42844485e-03],
        [ 2.62981975e-04,  9.81483906e-03,  1.65396181e+00],
        [-1.65871244e+00,  9.82002396e-02, -3.89705577e-04]])
    ```

    Compare this result with the *UB* matrix computed by SPEC:

    ```
    -1.658712442        0.09820024135       -0.000389705578
    -0.09554990312      -1.654278629        0.00242844486
    0.0002629818914     0.009815746824      1.653961812
    ```

    Same numbers, different row order.

1. set mode

    ```python
    fourc.calc.engine.mode = "constant_omega"
    ```

1. apply constraints

    ```python
    my_constraints = {
        # axis: Constraint(lo_limit, hi_limit, value, fit)
        "omega": Constraint(-180, 180, 0, False),
        # "chi": Constraint(-180, 180, 0, True),
        # "phi": Constraint(-180, 180, 0, True),
        # "tth": Constraint(-180, 180, 0, True),
    }
    fourc.applyConstraints(my_constraints)
    ```

1. calculate *(hkl)* given motor positions

    Given these motor positions, confirm this is the
    (2 2 1.9) reflection.

    axis | value
    --- | ---
    omega | 33.891
    chi | 145.985
    phi | 48.22875
    tth | 67.78225

    ```ipython
    In [170]: %mov fourc.omega 33.891 fourc.chi 145.985 fourc.phi 48.22875 fourc.tth 67.78225

    In [171]: fourc.wh()
    ===================== ==================
    term                  value
    ===================== ==================
    diffractometer        fourc
    mode                  constant_omega
    wavelength (angstrom) 1.239424258
    h                     1.9999956934724616
    k                     1.999999875673663
    l                     1.900000040364338
    omega                 33.891
    chi                   145.985
    phi                   48.22875
    tth                   67.78225
    ===================== ==================

    Out[171]: <pyRestTable.rest_table.Table at 0x7f46e069dd30>
    ```

1. compute the motor positions of the *(2 2 1.9)* reflection

    The previous (2 2 1.9) reflection is obviously not
    available in `constant_omega` mode with `omega=0`.  Observe
    that `tth ~ 2*omega` which is consistent with `bissector` mode.

    ```ipython
    In [181]: fourc.calc.engine.mode = "bissector"
        ...: fourc.showConstraints()
        ...:
    ===== ========= ========== ===== =====
    axis  low_limit high_limit value fit
    ===== ========= ========== ===== =====
    omega -180.0    180.0      0.0   False
    chi   -180.0    180.0      0.0   True
    phi   -180.0    180.0      0.0   True
    tth   -180.0    180.0      0.0   True
    ===== ========= ========== ===== =====
    ```

    The constraint on `omega` must be removed, then
    compute the default forward solution.

    ```ipython
    In [182]: fourc.undoLastConstraints()
        ...: print(fourc.forwardSolutionsTable(([2, 2, 1.9],)))
        ...:
    =========== ======== ========= ========= ======== =========
    (hkl)       solution omega     chi       phi      tth
    =========== ======== ========= ========= ======== =========
    [2, 2, 1.9] 0        -33.89115 -34.01497 48.22884 -67.78231
    =========== ======== ========= ========= ======== =========
    ```

    This does not match since both `omega` and `chi` are negative.
    Constrain all axes to non-negative values and recompute:

    ```python
    my_constraints = {
        # axis: Constraint(lo_limit, hi_limit, value, fit)
        "omega": Constraint(0, 180, 0, True),
        "chi": Constraint(0, 180, 0, True),
        "phi": Constraint(0, 180, 0, True),
        "tth": Constraint(0, 180, 0, True),
    }
    fourc.applyConstraints(my_constraints)
    ```

    Show the constraints.

    ```ipython
    In [204]: fourc.showConstraints()
    ===== ========= ========== ===== ====
    axis  low_limit high_limit value fit
    ===== ========= ========== ===== ====
    omega 0.0       180.0      0.0   True
    chi   0.0       180.0      0.0   True
    phi   0.0       180.0      0.0   True
    tth   0.0       180.0      0.0   True
    ===== ========= ========== ===== ====
    ```

    Summarize the diffractometer settings.

    ```ipython
    In [205]: fourc.wh()
    ===================== ==================
    term                  value
    ===================== ==================
    diffractometer        fourc
    mode                  bissector
    wavelength (angstrom) 1.239424258
    h                     2.0
    k                     2.0000000000000004
    l                     1.9000000000000001
    omega                 33.89115415842736
    chi                   145.9850300823625
    phi                   48.22884080585159
    tth                   67.78230831685472
    ===================== ==================

    Out[205]: <pyRestTable.rest_table.Table at 0x7f46da906a90>
    ```

    Print the default solution for *(2 2 1.9)*.

    ```ipython
    In [206]: print(fourc.forwardSolutionsTable(([2, 2, 1.9],)))
    =========== ======== ======== ========= ======== ========
    (hkl)       solution omega    chi       phi      tth
    =========== ======== ======== ========= ======== ========
    [2, 2, 1.9] 0        33.89115 145.98503 48.22884 67.78231
    =========== ======== ======== ========= ======== ========
    ```

    These values match exactly the values from the SPEC data file.

2. sample *(22l)* scan, near `l=1.9`

    First, get a simulated detector for the scans.
    (Pick the random signal from the ophyd simulators.)

    ```python
    from ophyd.sim import rand
    ```

    Next, scan *(22l)* near `l=1.9`:

    ```ipython
    In [209]: from ophyd.sim import rand

    In [210]: RE(bp.scan([rand], fourc.h, 2, 2, fourc.k, 2, 2, fourc.l, 1.8, 2.0, 11))


    Transient Scan ID: 205     Time: 2020-09-22 01:02:33
    Persistent Unique Scan ID: 'b6f83272-32ca-4361-846e-b995f4895d9b'
    New stream: 'baseline'
    New stream: 'primary'
    +-----------+------------+------------+------------+------------+-------------+------------+------------+------------+
    |   seq_num |       time |    fourc_h |    fourc_k |    fourc_l | fourc_omega |  fourc_chi |  fourc_phi |  fourc_tth |
    +-----------+------------+------------+------------+------------+-------------+------------+------------+------------+
    |         1 | 01:02:33.2 |      2.000 |      2.000 |      1.800 |      33.276 |    147.398 |     48.231 |     66.552 |
    |         2 | 01:02:33.4 |      2.000 |      2.000 |      1.820 |      33.397 |    147.112 |     48.231 |     66.793 |
    |         3 | 01:02:33.4 |      2.000 |      2.000 |      1.840 |      33.519 |    146.827 |     48.230 |     67.037 |
    |         4 | 01:02:33.4 |      2.000 |      2.000 |      1.860 |      33.642 |    146.545 |     48.230 |     67.283 |
    |         5 | 01:02:33.4 |      2.000 |      2.000 |      1.880 |      33.766 |    146.264 |     48.229 |     67.532 |
    |         6 | 01:02:33.4 |      2.000 |      2.000 |      1.900 |      33.891 |    145.985 |     48.229 |     67.782 |
    |         7 | 01:02:33.4 |      2.000 |      2.000 |      1.920 |      34.018 |    145.708 |     48.228 |     68.035 |
    |         8 | 01:02:33.4 |      2.000 |      2.000 |      1.940 |      34.145 |    145.433 |     48.228 |     68.290 |
    |         9 | 01:02:33.4 |      2.000 |      2.000 |      1.960 |      34.273 |    145.159 |     48.227 |     68.547 |
    |        10 | 01:02:33.4 |      2.000 |      2.000 |      1.980 |      34.403 |    144.887 |     48.227 |     68.806 |
    |        11 | 01:02:33.5 |      2.000 |      2.000 |      2.000 |      34.534 |    144.617 |     48.227 |     69.067 |
    +-----------+------------+------------+------------+------------+-------------+------------+------------+------------+
    generator scan ['b6f83272'] (scan num: 205)
    Out[210]: ('b6f83272-32ca-4361-846e-b995f4895d9b',)
    ```
