from taupy import satisfiability

def hd(pos1, pos2):
    """
    Hamming distance between two complete positions.
    It is not (yet) defined for partial positions.
    """
    if len(pos1) != len(pos2):
        raise ValueError("Hamming distance is defined for positions of equal length only")
    
    return len([k for k in pos1 if k in pos2 and pos1[k] != pos2[k]])

def bna(pos1, pos2):
    """
    General version of Betz' normalised agreement, which is the Hamming 
    distane normalised by the number of senteces under discussion.
    """
    return Fraction(hd(pos1, pos2), len(pos1))

def next_neighbours(_pos, _debate):
    """
    For the position _pos, find the "next door neighbours" in _debate.
    A next door neighbour is any position that, among all the positions in
    _debate, has a minimal HD to _pos.
    
    To pick a random next door neighbour, choose random.choice(next_neighbours())
    """
    _candidates = [i for i in satisfiability(_debate, all_models = True)]
    _distances = {_candidates.index(c): hd(_pos,c) for c in _candidates if hd(_pos,c) != 0}
    return [_candidates[i] for i in _distances if _distances[i] == min(_distances.values())]
