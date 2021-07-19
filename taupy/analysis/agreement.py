from fractions import Fraction
from taupy.basic.utilities import satisfiability, dict_to_prop, subsequences_with_length
from sympy import And
from sympy.logic.algorithms.dpll2 import dpll_satisfiable
from itertools import combinations, product, chain
from random import shuffle, choice
from math import comb
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

def edit_distance(pos1, pos2):
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

    return len([v for v in pos1.keys() | pos2.keys() if not (
        v in pos1 and 
        v in pos2 and 
        pos1[v] == pos2[v])])

def normalised_edit_distance(pos1, pos2):
    """
    The edit distance, normalised by the power of the union of the two positions' domains.
    """   
    return Fraction(len([v for v in pos1.keys() | pos2.keys() if not (
    v in pos1 and 
    v in pos2 and 
    pos1[v] == pos2[v])]), len(set(pos1.keys()).union(set(pos2.keys()))))

def kemeny_oppenheim(pos1, pos2):
    pass
        
def difference_measure(pos1, pos2):
    pass

def log_likelihood_measure(pos1, pos2):
    pass
    
def bna(pos1, pos2):
    """
    A normalised agreement measure, which is used by Betz (2012: 39). Here,
    agreement is understood as the inverse of the normalised Hamming distance.
    
    References
    ----------
    Betz, Gregor. 2013. Debate dynamics: How controversy improves our beliefs. 
    Springer. DOI: 10/d3cx
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