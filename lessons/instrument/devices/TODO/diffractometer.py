
"""add to capabilities of any diffractometer"""

__all__ = [
    'AxisConstraints',
    'DiffractometerMixin',
]

import collections
from ophyd import Component, Device
import pyRestTable

from ..session_logs import logger
logger.info(__file__)

AxisConstraints = collections.namedtuple(
    "AxisConstraints", 
    ("low_limit", "high_limit", "value", "fit"))


class DiffractometerMixin(Device):
    """
    add to capabilities of any diffractometer

    Provides:
    
    * applyConstraints()
    * resetConstraints()
    * showConstraints()
    * undoLastConstraints()
    * forwardSolutionsTable()
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._constraints_stack = []

    def applyConstraints(self, constraints):
        self._push_current_constraints()
        self._set_constraints(constraints)

    def resetConstraints(self):
        """set constraints back to initial settings"""
        if len(self._constraints_stack) > 0:
            self._set_constraints(self._constraints_stack[0])
            self._constraints_stack = []

    def showConstraints(self):
        tbl = pyRestTable.Table()
        tbl.labels = "axis low_limit high_limit value fit".split()
        for m in self.real_positioners._fields:
            tbl.addRow((
                m,
                *self.calc[m].limits,
                self.calc[m].value,
                self.calc[m].fit))
        print(tbl)

    def undoLastConstraints(self):
        if len(self._constraints_stack) > 0:
            self._set_constraints(self._constraints_stack.pop())

    def _push_current_constraints(self):
        constraints = {
            m: AxisConstraints(
                *self.calc[m].limits,
                self.calc[m].value,
                self.calc[m].fit)
            for m in self.real_positioners._fields
            # TODO: any other positioner constraints 
        }
        self._constraints_stack.append(constraints)

    def _set_constraints(self, constraints):
        for axis, constraint in constraints.items():
            self.calc[axis].limits = (constraint.low_limit, constraint.high_limit)
            self.calc[axis].value = constraint.value
            self.calc[axis].fit = constraint.fit

    # calculate using the current UB matrix & constraints
    def forwardSolutionsTable(self, reflections, full=False):
        """
        return table of computed solutions for each of supplied hkl reflections
        """
        _table = pyRestTable.Table()
        motors = self.real_positioners._fields
        _table.labels = "(hkl) solution".split() + list(motors)
        for reflection in reflections:
            try:
                solutions = self.calc.forward(reflection)
            except ValueError as exc:
                solutions = exc
            if isinstance(solutions, ValueError):
                row = [reflection, "none"]
                row += ["" for m in motors]
                _table.addRow(row)
            else:
                for i, s in enumerate(solutions):
                    row = [reflection, i]
                    row += [f"{getattr(s, m):.5f}" for m in motors]
                    _table.addRow(row)
                    if not full:
                        break   # only show the first (default) solution
        return _table
