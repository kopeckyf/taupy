import numpy as np

def difference_matrix(positions, measure):
    """
    Create a difference profile for the given positions relative to a measure.
    """
    return np.array([[measure(i, j) for j in positions] for i in positions])

def spread(positions, measure):
    """
    The simplest distance measure consists in measuring the diameter of 
    positions.

    So this is simply the maximum value in the distance matrix.
    """
    return np.amax(difference_matrix(positions, measure))