import numpy as np
import numpy.ma as ma
from fractions import Fraction
from math import sqrt, log
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
    l = []
    for c in clusters:
        neighbours = adjacency_matrix[np.ix_(c, c)]
        l.append(neighbours[~np.eye(len(neighbours), dtype=bool)].mean())
    return 1 - sum(l)/len(l)

def group_size_parity(clusters):
    """
    Bramson et al.'s measure of (group) size parity, adjusted to TDS.

    WARNING: Need to contact the authors for what they mean by "population 
             proportions". Maybe we need to use len(c)/G instead of len(c)
             below!
    """
    G = number_of_groups(clusters)
    return -1 / log(G) * sum([len(c) * log(len(c)) for c in clusters])