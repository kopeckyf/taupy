import numpy as np
import numpy.ma as ma
from fractions import Fraction
from math import sqrt, log
from sympy import symbols
from taupy.basic.utilities import (neighbours_of_list, iter_to_string, 
                                   graph_from_positions)


def groups_from_stance_toward_single_proposition(positions, proposition):
    """
    Returns a clustering of the input ``positions`` to a single ``proposition``.

    The first sublist contains the ``positions`` that assert ``proposition``, 
    the second sublist those that deny it.
    """
    q = symbols(proposition)
    return [[n for n, p in enumerate(positions) if p[q] == True], 
            [n for n, p in enumerate(positions) if p[q] == False]]

def difference_matrix(positions, measure):
    """
    Create a quadratic matrix $D_{ij}$ in which rows and columns are filled by
    ``positions``. The value at $D_{ij}$ is the distance, 
    calculated by ``measure``, between positions $i$ and $j$.
    
    This matrix of distances is the fundamental object to calculate most 
    polarisation measures.
    """
    return np.array([[measure(i, j) for j in positions] for i in positions])

def spread(positions, measure):
    """
    Returns the maximum distance between any two of the ``positions`` 
    relative to a ``measure``.
    
    References
    ----------
    Bramson, Aaron et al. 2016. Disambiguation of social polarization concepts
    and measures. In The Journal of Mathematical Sociology 40(2), pp. 80--111.
    DOI: 10/d3kn.
    """
    return np.amax(difference_matrix(positions, measure))

def pairwise_dispersion(positions, measure):
    """
    Returns dispersion, understood as the standard deviation of pairwise 
    distances between the ``positions`` relative to the ``measure``.
    
    This is the TDS equivalent of statistical dispersion or variance in 
    polling data. Beside standard deviation, there are other ways of measuring
    dispersion.
    
    Bramson et al. take the dispersion relative to a mean. However, since such
    a mean is not well-defined in TDS, we use dispersion on pairwise relations
    instead.

    For this purpose, we use the upper triangle of the difference matrix, 
    without the diagonal zeroes (this offset is controlled by ``k=1``). 
    Since $D_{a,b} = D_{b,a}$, these are the pairwise difference values we are 
    after. We then take the standard deviation of these values.
    
    References
    ----------
    Bramson, Aaron et al. 2016. Disambiguation of social polarization concepts
    and measures. In The Journal of Mathematical Sociology 40(2), pp. 80--111.
    DOI: 10/d3kn.
    """
    return sqrt(difference_matrix(positions, measure)[np.triu_indices(
        len(positions), k=1)].var())

def lauka(positions):
    """
    An implementation of Lauka's et al. measure of *mass political polarisation*,
    adapted to TDS.
    
    0.25 is the maximum value that the ``sum(l)/num_issues`` can take. The Lauka
    measure is thus a relation of actual compared to maximal value.
    
    References
    ----------
    Lauka, Alban et al. 2018. Mass partisan polarization: Measuring a relational 
    concept. American Behavioral Scientist 62(1). 107–126. 
    DOI: 10.1177/0002764218759581
    """
    issues = {j for i in positions for j in i.keys()}
    num_positions = len(positions)
    num_issues = len(issues)
    l = []
    
    for i in issues:
        x = 0
        y = 0
        for p in positions:
            if p[i] == True:
                x += 1
            if p[i] == False:
                y += 1
        l.append((x/num_positions) * (y/num_positions))
    
    return (sum(l)/num_issues) / 0.25

def number_of_groups(clustering):
    return np.shape(clustering)[0]

def group_divergence(clusters, adjacency_matrix):
    """
    A variant of Bramson et al.'s group divergence, adapted to TDS. 
    
    Group divergence relies on a useful clustering that returns ``clusters``, 
    which is expected to be a list of lists. The ``adjacency_matrix`` can be a 
    modified or scaled version of ``difference_matrix()``, or the verbatim matrix.
    
    Algorithms which are known to being able to return good results in TDS are:
    
     - Leiden (implementation from ``python-igraph``) and other modularity 
       maximisation approaches.
     - Affinity propagation (implementation from ``scikit-learn``).
     - Agglomerative clustering (implementation from ``scikit-learn``).
 
    References
    ----------
    Bramson, Aaron et al. 2016. Disambiguation of social polarization concepts
    and measures. In The Journal of Mathematical Sociology 40(2), pp. 80--111.
    DOI: 10/d3kn.
    """
    l = []
    for c in clusters:
        # Let's create a mask to detect the values of neighbours.
        mask_of_neighbours = ma.ones(adjacency_matrix.shape)  
        # The mask should include the cross product of neighbours.
        mask_of_neighbours[np.ix_(c, c)] = 0
        # But not the relations of one neighbour to itself. Those are
        # stored on the diagonal, and so we take it out.
        np.fill_diagonal(mask_of_neighbours, 1)
        neighbours = ma.array(adjacency_matrix, mask=mask_of_neighbours, copy=True)
        # Now do the inverse operation for strangers. Instead of a 
        # matrix of Ones, we start with one of Zeros.
        strangers_indices = list(set(range(len(adjacency_matrix))) - set(c))
        mask_of_strangers = ma.zeros(adjacency_matrix.shape)
        # And this time, neighbours are masked instead of unmasked.
        mask_of_strangers[np.ix_(c, c)] = 1
        mask_of_strangers[np.ix_(strangers_indices, strangers_indices)] = 1
        np.fill_diagonal(mask_of_strangers, 1)
        strangers = ma.array(adjacency_matrix, mask=mask_of_strangers, copy=True)

        if neighbours.count() > 1 and strangers.count() > 0:
            # Every cluster has at least one member -- or it wouldn't be a cluster, hence 
            # the check for neighbours.count() > 1.
            l.append(abs(neighbours.mean() - strangers.mean()))
        else:
            if(strangers.count() > 1):
                l.append(neighbours.mean())
            if(strangers.count() > 0):
                l.append(strangers.mean())
            if(neighbours.count() == 1 and strangers.count() == 0):
                l.append(0)
        
    try:
        return sum(l)/len(l)
    except ZeroDivisionError:
        return float("nan")

def group_consensus(clusters, adjacency_matrix):
    """
    A variant of Bramson et al.'s measure of group consensus, adapted to TDS.
    
    As ``group_divergence()``, this relies on a good clustering as well. 
    Arguments and recommentations for algorithms to try are the same as in
    ``group_divergence()``.
    
    References
    ----------
    Bramson, Aaron et al. 2016. Disambiguation of social polarization concepts
    and measures. In The Journal of Mathematical Sociology 40(2), pp. 80--111.
    DOI: 10/d3kn.
    """
    l = []
    for c in clusters:
        neighbours = adjacency_matrix[np.ix_(c, c)]
        try:
            l.append(neighbours[~np.eye(len(neighbours), dtype=bool)].mean())
        except ZeroDivisionError:
            l.append(0)
    try:
        return 1 - sum(l)/len(l)
    except ZeroDivisionError:
        return float("nan")

def group_size_parity(clusters):
    """
    Bramson et al.'s measure of (group) size parity, adjusted to TDS. According
    to the authors, size parity is an entropy measure, which is irrespective of
    the size of the population and of the number of groups. It is said to behave
    erratically in case the groups are determined endogenously, e.g. by one of
    the clustering algorithms Leiden, Affinity propagation, etc.

    References
    ----------
    Bramson, Aaron et al. 2016. Disambiguation of social polarization concepts
    and measures. In The Journal of Mathematical Sociology 40(2), pp. 80--111.
    DOI: 10/d3kn.
    """
    # Catch empty clusters (applicable to the exogenous group detection)
    clusters = [c for c in clusters if c]
    G = number_of_groups(clusters)
    population_size = sum([len(c) for c in clusters])
    try:
        return -1 / log(G) * sum([len(c)/population_size * log(
            len(c)/population_size) for c in clusters])
    except ZeroDivisionError:
        return float("nan")
