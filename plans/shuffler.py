#!/usr/bin/env python

"""
"""


def bisection_shuffle(sequence):
    """
    shuffle a list by bisection
    
    Example 1::
    
        given:   ['a', 'b', 'c', 'd']
        returns: ['a', 'c', 'd', 'b']
    
    Example 2::
    
        given:   ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        returns: ['a', 'e', 'g', 'c', 'h', 'i', 'f', 'd', 'b']

    """
    indices = []
    if len(sequence) > 0:
        # work with an integer list of indices
        indices0 = list(range(len(sequence)))
        # ALWAYS use the first point first
        indices.append(indices0.pop(0))
        trail = _traverse_(indices0)

        if trail is not None:
            for trace in sorted(trail, reverse=True):
                length, mid_pt, lo, hi = trace
                indices.append(mid_pt)

    return [sequence[i] for i in indices]


def _traverse_(sequence):
    if sequence is None or len(sequence) == 0:
        return None
    mid_pt, lo, hi = _bisector_(sequence)
    trail = []
    trail.append( ((len(lo) + len(hi))/2, mid_pt, lo, hi) )
    for part in (lo, hi):
        trace = _traverse_(part)
        if trace is not None:
            trail += trace
    return trail


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
    for n in range(len(base)):
        arr = base[:n]
        print(n, bisection_shuffle(arr))
