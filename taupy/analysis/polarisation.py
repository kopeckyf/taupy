import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
import numpy as np
from fractions import Fraction
from math import sqrt

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
    
    return sum(l) / num_issues

def generate_groups(positions, algorithm=greedy_modularity_communities):
    return algorithm(nx.from_dict_of_lists(positions))

def group_divergence(debate, measure, group_algorithm=greedy_modularity_communities):
    """
    A variant of Bramson et al.'s group divergence, adapted to TDS. 
    This can be regarded as an aggregated measure of the mean dispersion measure,
    but this one accounts for groups. 
    """
    graph, tvmap = debate.sccp(return_attributions=True)
    # Protect against x/0. 
    # Unfortunately in Python, 0/0 != 0, which would be convenient here.  
    try:
        groups = generate_groups(graph, algorithm=group_algorithm)
        population = set().union(*groups)
        l = []
        for g in groups:
            subpopulation = set(g)
            for member in g:
                neighbours = [measure(tvmap[member], tvmap[i]) for i in set(subpopulation - {member})]
                strangers = [measure(tvmap[member], tvmap[j]) for j in set(population - subpopulation)]
                if neighbours and strangers:
                    # Control if the positions has neighbours and strangers
                    l.append(abs(sum(neighbours)/len(neighbours) - sum(strangers)/len(strangers)))
                else:
                    # If not, protect against n/0 by running through all the other possibilities.
                    if strangers:
                        l.append(sum(strangers)/len(strangers))
                    if neighbours:
                        l.append(sum(neighbours)/len(neighbours))
                    if not strangers and not neighbours:
                        l.append(0)
        return sum(l) / len(graph)
    except ZeroDivisionError:
        return 0

def group_consensus(debate, measure, group_algorithm=greedy_modularity_communities):
    """
    A variant of Bramson et al.'s measure of group consensus, adapted to TDS.
    """
    graph, tvmap = debate.sccp(return_attributions=True)
    try:
        groups = generate_groups(graph, algorithm=group_algorithm)
        l = [pairwise_dispersion([tvmap[member] for member in g], measure) for g in groups]
        return 1 - sum(l)/len(l)
    except ZeroDivisionError:
        return 0
        
