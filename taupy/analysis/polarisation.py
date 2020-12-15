import numpy as np
from fractions import Fraction

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

def dispersion_mean_pairwise(positions, measure):
    """
    This measure is the TDS equivalent of statistical dispersion or variance in polling data. There are many different ways to measure mean dispersion.

    For this purpose, we use the upper triangle of the difference matrix, without the diagonal zeroes (this offset is controlled by k=1). Since d(a,b) = d(b,a), these are the pairwise difference values we are after. We then take the mean of these values with np.mean().
    """
    return difference_matrix(positions, measure)[np.triu_indices(
        len(positions), k=1)].mean()

def lauka(positions):
    """
    Lauka's et al. (2018) mass political polarisation measure, adapted to TDS.

    ----
    References:
    Lauka, Alban, Jennifer McCoy & Rengin B. Firat. 2018. Mass partisan polarization: Measuring a relational concept. American Behavioral Scientist 62(1). 107–126. DOI: 10.1177/0002764218759581
    """
    _n = len(positions)
    _issues = {i.keys() for i in positions}
    l = []

    for i in _issues:
        x = 0
        y = 0
        for p in positions:
            if p[i] == True:
                x += 1
            if p[i] == False:
                y += 1
        l.append(Fraction(x, _n) * Fraction(y, _n))
    
    return Fraction(sum(l), Fraction(_n-1, _n))