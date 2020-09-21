Four-circle Diffractometer Demonstration

Setup a four-circle diffractometer using the *hkl* package.

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

```
import gi
gi.require_version('Hkl', '5.0')
```

Next, import the desired diffractometer geometry from the
[*hklpy*](https://github.com/bluesky/hklpy) package.  We pick
`E4CV` (Eulerian 4-Circle with Vertical scattering geometry)
as is typical at synchrotron beam lines.

```
from hkl.diffract import E4CV
from hkl.util import Lattice
```

Next, we get additional packages that we may use.

```
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

```
class FourCircleDiffractometer(DiffractometerMixin, E4CV):
    h = Component(PseudoSingle, '', labels=("hkl", "fourc"))
    k = Component(PseudoSingle, '', labels=("hkl", "fourc"))
    l = Component(PseudoSingle, '', labels=("hkl", "fourc"))

    omega = Component(SoftPositioner, labels=("motor", "fourc"))
    chi =   Component(SoftPositioner, labels=("motor", "fourc"))
    phi =   Component(SoftPositioner, labels=("motor", "fourc"))
    tth =   Component(SoftPositioner, labels=("motor", "fourc"))
```

Create the diffractometer object:

```
fourc = FourCircleDiffractometer('', name='fourc')
```

The `fourc.wh()` method provides a quick summary of
the diffractometer:

```
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

```
In [54]: print(fourc.omega)
SoftPositioner(name='fourc_omega', parent='fourc', settle_time=0.0, timeout=None, egu='', limits=(0, 0), source='computed')

In [55]: print(fourc.omega.position)
None
```

Since `omega` was just created (see `SoftPositioner` above), it has no
value yet.  Use the `%mov` magic to set its value:

```
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

```
In [21]: fourc.calc.engine.mode
Out[21]: 'bissector'
```

Print the list of available operating modes:
```
In [22]: print(fourc.engine.modes)
['bissector', 'constant_omega', 'constant_chi', 'constant_phi', 'double_diffraction', 'psi_constant']
```

Change to `constant_phi` mode:

```
In [29]: fourc.calc.engine.mode = "constant_phi"

In [30]: fourc.calc.engine.mode
Out[30]: 'constant_phi'
```

Change it back:

```
In [31]: fourc.calc.engine.mode = "bissector"

In [32]: fourc.calc.engine.mode
Out[32]: 'bissector'
```

## Wavelength

The default wavelength is `1.54` angstroms.

```
In [23]: fourc.calc.wavelength
Out[23]: 1.54
```

Change the wavelength (use angstrom):

```
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

```
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

```
fourc.calc.new_sample('orthorhombic',
    lattice=Lattice(
        a=1, b=2, c=3,
        alpha=90.0, beta=90.0, gamma=90.0))
```

Now, there are two samples defined.  The `fourc.calc.sample` symbol
points to the new one:

```
In [49]: len(fourc.calc._samples)
Out[49]: 2

In [50]: print(fourc.calc.sample.name)
orthorhombic
```

Switch back to the `main` sample:

```
In [51]: fourc.calc.sample = "main"

In [52]: print(fourc.calc.sample.name)
main
```

Let's work with this sample now:

```
fourc.calc.new_sample('EuPtIn4_eh1_ver', 
    lattice=Lattice(
        a=4.542, b=16.955, c=7.389, 
        alpha=90.0, beta=90.0, gamma=90.0))
```

## Orientation

This is the orientation matrix defined by default:

```
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

```
In [80]: fourc.calc.sample.U = [[0, 1, 0], [0,0,1], [1,0,0]]

In [81]: fourc.calc.sample.U
Out[81]:
array([[0., 1., 0.],
       [0., 0., 1.],
       [1., 0., 0.]])
```
Set it back:

```
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

```
position = fourc.calc.Position(
        omega=22.31594, chi=89.1377, phi=0, tth=45.15857)
r1 = fourc.calc.sample.add_reflection(0, 8, 0, position=position)
```

Define a second reflection (that is not a multiple
of the first reflection):

```
r2 = fourc.calc.sample.add_reflection(
    0, 12, 1,
    position=fourc.calc.Position(
        omega=34.96232, chi=78.3139, phi=0, tth=71.8007))
```

Calculate the *UB* matrix from these two reflections:

```
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

```
In [97]: print(fourc.forwardSolutionsTable([[1,0,0],[0,1,0]]))
========= ======== ======== ======== ========= ========
(hkl)     solution omega    chi      phi       tth     
========= ======== ======== ======== ========= ========
[1, 0, 0] 0        10.32101 0.20845  86.38310  20.64202
[0, 1, 0] 0        2.75098  89.09839 -16.98330 5.50196 
========= ======== ======== ======== ========= ========
```

Show *all* the possible solutions by adding the `full=True` keyword:

```
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

```
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

The `forwardSolutionsTable` does not raise an 
error but displays `none` for that *hkl* reflection:

```
In [121]: print(fourc.forwardSolutionsTable( [ [5,4,35], ], full=True))
========== ======== ===== === === ===
(hkl)      solution omega chi phi tth
========== ======== ===== === === ===
[5, 4, 35] none                      
========== ======== ===== === === ===
```

## Constraints

Constraints are applied to restrict the range of allowed 
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

Apply a constraint that limits `phi >= 0`:

```
my_constraints = {
    "omega": Constraint(0, 180, 0, True)
}
fourc.applyConstraints(my_constraints)
```

```
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

```
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

```
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

Reset all the above changes by re-creating the `fourc` object.

```
fourc = FourCircleDiffractometer('', name='fourc')
```

TODO:

1. define sample
2. set wavelength
3. set mode
4. define two reflections
5. calc UB matrix
6. apply constraints
7. sample *(00l)* scan
