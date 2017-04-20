#!/usr/bin/env python

"""
"""

from math import log2


def bisection_shuffle(sequence):
    """
    shuffle a list by bisection
    
    Example 1::
    
        given:   ['a', 'b', 'c', 'd']
        returns: ['a', 'c', 'd', 'b']
    
    Example 2::
    
        given:   ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        returns: ['a', 'e', 'g', 'c', 'h', 'i', 'b', 'f', 'd']

    """
    indices = []
    if len(sequence) > 0:
        # work with an integer list of indices
        indices0 = list(range(len(sequence)))
        # ALWAYS use the first point first
        indices.append(indices0.pop(0))
        trail = _traverse_(indices0, 0.1)

        if trail is not None:
            indices += [trace[1] for trace in sorted(trail, reverse=True)]

    return [sequence[i] for i in indices]


def _traverse_(sequence, trace_weight):
    if sequence is None or len(sequence) == 0:
        return None
    mid_pt, lo, hi = _bisector_(sequence)
    trail = []
    weight = (len(lo) + len(hi))/2 - trace_weight
    trail.append( (weight, mid_pt) )
    trace_weight /= 3
    for part in (lo, hi):
        trace = _traverse_(part, trace_weight/10)
        if trace is not None:
            trail += trace
            trace_weight *= 2
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


def _recombine_bisection_log2(offsets):
    """
    combine a list of offset duos by all permutations
    
    returns a 1-D list of numbers
    """
    if len(offsets) == 1:
        return offsets[0]
    return [i+j for j in _recombine_bisection_log2(offsets[1:]) for i in offsets[0]]


def bisection_shuffle_log2(sequence):
    """
    return a bisection permutation of the sequence, based on the log2 function
    
    example 1::
    
        sequence = [0 1 2 3 4 5 6 7 8 9 10 11 12 13]
        returns [0, 8, 4, 12, 2, 10, 6, 1, 9, 5, 13, 3, 11, 7]
    
    example 2::
    
        sequence = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
        returns [1.1, 1.9, 1.5, 1.3, 1.7, 1.2, 2.0, 1.6, 1.4, 1.8]
    
    """
    offsets = []        # list of offset duos:  [(i1, i2), (i1, i2), (i1, i2)]
    mid = 1 << int(log2(len(sequence)))        # 2^log2(numPts)
    while mid > 0:
        offsets.append((0, mid))
        mid = int(mid/2)
    
    r = _recombine_bisection_log2(offsets)
    remap = [i for i in r if i < len(sequence)]
    return [sequence[i] for i in remap]
