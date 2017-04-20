#!/usr/bin/env python

"""
"""


def bisection_shuffle(sequence):
    """
    shuffle a list by bisection
    
    Example 1::
    
        given:   ['a', 'b', 'c', 'd']
        returns: ['a', 'c', 'b', 'd']
    
    Example 2::
    
        given:   ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        returns: ['a', 'e', 'c', 'b', 'd', 'g', 'f', 'h', 'i']

    """
    indices = []
    if len(sequence) > 0:
        # work with an integer list of indices
        indices0 = list(range(len(sequence)))
        # ALWAYS use the first point first
        indices.append(indices0.pop(0))
        _traverse_(indices0, indices)
    return [sequence[i] for i in indices]


def _traverse_(sequence, indices):
    if len(sequence) > 0:
        mid_pt, lo, hi = _bisector_(sequence)
        if mid_pt >= 0:
            indices.append(mid_pt)
            _traverse_(lo, indices)
            _traverse_(hi, indices)


def _bisector_(sequence):
    """
    divide sequence into tuple of: `[] mid_pt []`
    """
    lo = []
    hi = []
    mid_pt = ((len(sequence)+1) // 2) - 1
    if mid_pt > 0:
        lo = sequence[:mid_pt]
    if mid_pt < len(sequence)-1:
        hi = sequence[mid_pt+1:]
    return sequence[mid_pt], lo, hi


if __name__ == '__main__':
    base = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.split()
    for n in range(15):
        arr = base[:n]
        print(n, bisection_shuffle(arr))
