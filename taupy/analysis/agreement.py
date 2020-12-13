from fractions import Fraction
from taupy.basic.utilities import satisfiability

def hamming_distance(pos1, pos2):
    """
    Hamming distance between two complete positions. The Hamming distance can 
    be interpreted as a special case of edit_distance with the specialisation of 
    only allowing substitions. This is why the Hamming distance for positions 
    can only be calculated for positions with the same domain.
    """
    if pos1.keys() != pos2.keys():
        raise ValueError("Hamming distance is only defined for positions \
                          of the same domain.")
    
    return len([k for k in pos1 if pos1[k] != pos2[k]])

def normalised_hamming_distance(pos1, pos2):
    """
    The Hamming distanced, normalised by the positions' domain.
    """
    return Fraction(len([k for k in pos1 if pos1[k] != pos2[k]]), len(pos1))

def edit_distance(pos1, pos2):
    """
    A generalised distance measure that does not require the positions to be
    of equal length. Compared to edit distances for ordered sequences (e.g. 
    Leventsthein distance), it is far easier to compare two iterables. 
    
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
    There are different interpretations whether, e.g., substition would be weighted
    at 0.5 and the other two at 1.
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
    General version of Betz' normalised agreement, which is the Hamming 
    distane normalised by the number of senteces under discussion.
    """
    return 1 - Fraction(hamming_distance(pos1, pos2), len(pos1))

def next_neighbours(_pos, _debate):
    """
    For the position _pos, find the "next door neighbours" in _debate.
    A next door neighbour is any position that, among all the positions in
    _debate, has a minimal HD to _pos.
    
    To pick a random next door neighbour, choose random.choice(next_neighbours())
    """
    _candidates = [i for i in satisfiability(_debate, all_models = True)]
    _distances = {_candidates.index(c): edit_distance(_pos,c) for c in _candidates if edit_distance(_pos,c) != 0}
    return [_candidates[i] for i in _distances if _distances[i] == min(_distances.values())]