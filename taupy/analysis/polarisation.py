import numpy as np
from fractions import Fraction
from math import sqrt
from taupy.basic.utilities import neighbours_of_list, iter_to_string, graph_from_positions

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

def pairwise_dispersion(positions, measure):
    """
    This measure is the TDS equivalent of statistical dispersion or variance in polling data. There are many different ways to measure mean dispersion.

    For this purpose, we use the upper triangle of the difference matrix, without the diagonal zeroes (this offset is controlled by k=1). Since d(a,b) = d(b,a), these are the pairwise difference values we are after. We then take the mean of these values with np.mean().
    """
    return sqrt(difference_matrix(positions, measure)[np.triu_indices(
        len(positions), k=1)].var())

def lauka(positions):
    """
    Lauka's et al. (2018) mass political polarisation measure, adapted to TDS.

    ----
    References:
    Lauka, Alban, Jennifer McCoy & Rengin B. Firat. 2018. Mass partisan polarization: Measuring a relational concept. American Behavioral Scientist 62(1). 107–126. DOI: 10.1177/0002764218759581
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
        l.append((x / num_positions) * (y / num_positions))
    
    return (sum(l) / num_issues) / 0.25

def number_of_groups(clustering):
    return np.shape(clustering)[0]

def group_divergence(clusters, adjacency_matrix):
    """
    A variant of Bramson et al.'s group divergence, adapted to TDS. 
    This can be regarded as an aggregated measure of the mean dispersion measure,
    but this one accounts for groups. 
    """
    l = []
    for c in clusters:
        # With numpy.ix_, we can create a c*x adjacency sub-matrix that
        # has only the relations as indexed by the current cluster.
        neighbours = adjacency_matrix[np.ix_(c, c)]
        # For the mean, we take out the diagonal.
        mean_of_neighbours = neighbours[~np.eye(len(neighbours, dtype=bool))].mean()
        # We use np.setdiff1d to do the same for the (n-c)*(n-c) sub-matrix
        # of strangers. We can use len() here b/c the adjacency matrix is 
        # always quadratic.
        s = np.setdiff1d(c, np.array(len(adjacency_matrix)))
        strangers = adjacency_matrix[np.ix_(s, s)]
        mean_of_strangers = strangers.mean()

        if len(neighbours) > 1 and len(strangers) > 0:
            # Every cluster has at least one member -- or it wouldn't be a cluster, hence 
            # the check for len(neighbours) > 1.
            l.append(abs(mean_of_neighbours - mean_of_strangers))
        else:
            if(len(neighbours) > 1):
                l.append(mean_of_neighbours)
            if(len(strangers) > 0):
                l.append(mean_of_strangers)
            if(len(neighbours) == 1 and len(strangers) == 0):
                l.append(0)
        
    if sum(l) > 0:
        return sum(l)/len(l)
    else:
        # A zero result always means that no clusters were found or the population conists
        # of just one member.
        return 0

def group_consensus(clusters, adjacency_matrix):
    """
    A variant of Bramson et al.'s measure of group consensus, adapted to TDS.
    """
    try:
        l = []
        for c in clusters:
            neighbours = adjacency_matrix[np.ix_(c, c)]
            l.append(neighbours[~np.eye(len(neighbours, dtype=bool))].mean())
        return 1 - sum(l)/len(l)
    except ZeroDivisionError:
        return 0