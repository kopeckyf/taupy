from fractions import Fraction
from taupy.basic.utilities import subsequences_with_length
import numpy as np

def hamming_distance(pos1, pos2):
    """
    Returns the Hamming distance between two positions of equal length. 
    The Hamming distance counts the number of differences in truth-value 
    attributions. This distance can only be calculated for positions with 
    the same domain (complete positions on the same debate have the same domain).
    """
    if pos1.keys() != pos2.keys():
        raise ValueError("Hamming distance is only defined for positions \
                          of the same domain.")
    
    return len([k for k in pos1 if pos1[k] != pos2[k]])

def normalised_hamming_distance(pos1, pos2):
    """
    Returns the Hamming distance normalised by the number of propositions in the 
    positions' domain.
    """
    return Fraction(len([k for k in pos1 if pos1[k] != pos2[k]]), len(pos1))

def edit_distance(pos1, pos2, weights = {"substitution": 1.0, 
                                         "insertion": 1.0, 
                                         "deletion": 1.0}):
    """
    A generalised distance measure that does not require that the positions
    share their domain. Compared to edit distances for ordered sequences (e.g. 
    Leventsthein distance), it is far easier to compare two positions in terms
    of TDS:
    
    For each item, two positions can have four states:
     - They agree on the item, which does not increase the distance
     
    There are three operations that do increase the distance:
     - Substitution:
       The positions are equal after transposition, i.e. changing a truth-value
     - Insertion:
       One position does not make a statement concerning one proposition. Adding
       the respective truth-value attribution makes the two positions equal w.r.t
       the statement.
     - Deletion:
       One position does make a statement that the other does not care about. 
       The positions can be made equal if the first position forgets its statement.
    
    In the following measure, these operations are all weighted with factor 1. 
    Another implementation is needed to factor in different weights.
    """ 
    n_subsitutions = 0
    n_insertions = 0
    n_deletions = 0

    # We're doing the search “on foot”. This may seem a little pedestrian,
    # but it's a good idea since we have to parse the dictionary only once.
    for v in set(pos1.keys()) | set(pos2.keys()):
        # Substituion: Neither position suspends on the proposition,
        #              but they also don't agree.
        if v in pos1 and v in pos2 and pos1[v] != pos2[v]:
            n_subsitutions += 1
        # Insertion: The first position suspends, the second doesn't.
        if v not in pos1 and v in pos2: n_insertions += 1
        # Deletion: The first position doesn't suspend, but the 
        #           second does.
        if v in pos1 and v not in pos2: n_deletions += 1
    
    return (n_subsitutions * weights["substitution"] 
            + n_insertions * weights["insertion"] 
            + n_deletions * weights["deletion"])

def normalised_edit_distance(pos1, pos2, weights = {"substitution": 1.0, 
                                                    "insertion": 1.0, 
                                                    "deletion": 1.0}):
    """
    The (weighted) edit distance, normalised to return a value in [0, 1].
    Normalisation is understood as the relation between actual and maximal
    difference. Maximal difference is achieved in the edit distance if the
    most costly action is performed for all items.
    """

    # Special case: The edit distance between two empty positions
    if 0 == len(set(pos1.keys()).union(set(pos2.keys()))):
        return 0
    else: 
        max_n_operations = (max(weights.values())
                            * len(set(pos1.keys()).union(set(pos2.keys()))))

        return edit_distance(pos1, pos2, weights=weights) / max_n_operations

def normalised_edit_agreement(pos1, pos2):
    """
    An agreement function based on the normalised edit distance is defined for 
    convenience. It equals $1-\text{normalised ED}(x,y)$.
    """
    return 1 - normalised_edit_distance(pos1, pos2)

def kemeny_oppenheim(pos1, pos2):
    pass
        
def difference_measure(pos1, pos2):
    pass

def log_likelihood_measure(pos1, pos2):
    pass
    
def bna(pos1, pos2):
    """
    A normalised agreement measure for positions of equal length, which is 
    used by [Betz2013]_, page 39. Here, agreement is normalised to the length 
    of the positions.
    """
    return 1 - normalised_hamming_distance(pos1, pos2)

def next_neighbours(pos, *, debate, models):
    """
    For the position ``pos``, find the "next door neighbours" in ``debate``.
    A next door neighbour is any position that, among all the positions in
    ``debate``, has a minimal Hamming distance to ``pos``.
    
    Maybe the most natural implementation of this search would be a top-down
    approach: Obtain all the candidates and return those with minimum distance.

    However, this is prohibitively expensive. A better search is to do bottom-up,
    starting with candidates that have distance 1, checking whether there are some
    that are coherent, and looping until the maximum distance is checked. 
    """
    pos_debate_union = {k: pos[k] for k in pos if k in debate.atoms()}
    distances_to_candidates = np.array([hamming_distance(i, pos_debate_union) for i in models])

    return [models[i] for i in np.where(distances_to_candidates == distances_to_candidates.min())[0].tolist()]

def switch_deletion_neighbourhood(position, distance):
    """
    Determine the neighbourhood of edit distance equal to ``distance`` or a ``position``.
    The operations allowed here for the edit distance are removal and switching of a TVA. 
    This function is intended to be used in finding alternatives for non-coherent partial positions.
    This is why the function does not look for additions in the edit distance: if a partial position
    is incoherent, so is every extension of this position. 

    Returns a list of candidates for further inspection (e.g. for closedness).
    """

    candidates = []

    for i in subsequences_with_length(position.keys(), distance):
        for k in subsequences_with_length(set(position.keys())-set(i), distance-len(i)):
            candidates.append((i, k))

    for c in candidates:
        if (not (set(c[0]) & set(c[1]))) and (len(set(c[0]) | set(c[1])) == distance):
            yield c

def ncc(population, *, agent, measure=hamming_distance):
    """
    Returns the normalised closedness centrality (NCC) of an :py:attr:`agent`
    in a :py:attr:`population` relative to a :py:attr:`measure` 
    (see [Betz2013]_, Section 2.4). 
    
    :param population: Iterable containing agents' belief systems.
    
    :param agent: A single belief system.
    
    :param measure: A distance measure between belief systems.
    """
    n = len(population) - 1
    d = 2 * sum([measure(agent, p) for p in population])

    try:
        return n/d
    except ZeroDivisionError:
        # There is 100% agreement in the population
        return float("inf")

def average_ncc(population, *, measure=hamming_distance):
    """
    Population-wide average of the normalised closedness centrality.
    """
    n = sum([ncc(population, agent=p, measure=measure) for p in population])
    d = len(population)

    return n/d

def difference_matrix(positions, measure):
    """
    Create a quadratic matrix $D_{ij}$ in which rows and columns are filled by
    ``positions``. The value at $D_{ij}$ is the distance, 
    calculated by ``measure``, between positions $i$ and $j$.

    This matrix of distances is the fundamental object to calculate most 
    polarisation measures.
    """
    return np.array([[measure(i, j) for j in positions] for i in positions])
