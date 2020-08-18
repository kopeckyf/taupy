def hd( pos1, pos2 ):
    """
    Hamming distance between two complete positions.
    But what to do about partial positions?
    """
    if len(pos1) != len(pos2):
        raise ValueError("Hamming distance is defined for positions of equal length only")
    
    return len([k for k in pos1 if k in pos2 and pos1[k] == pos2[k]])

def bna( pos1, pos2 ):
    """
    General version of Betz' normalised agreement, which is the Hamming distane
    normalised by the number of senteces under discussion.
    """
    return Fraction(hd(pos1, pos2), len(pos1))
