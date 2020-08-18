def dict_to_prop(dictionary):
    """
    Helper function that converts a dictionary to a propositional formula, 
    acknowledging dictionary's truth-value attributions.
    """
    _l = []
    for (k, v) in dictionary.items():
        if v == True: _l.append(k)
        if v == False: _l.append(Not(k))
    return And(*_l)

def list_to_string(l):
    """
    Helper function that converts a dictionary position to a bit string.
    """
    return "".join(str(i) for i in l)

def neighbours_of_list(l):
    """
    Find the neighbours of a position in list format. A neighbour is a position
    that has HD = 1 to the position in question.
    """
    _complements = [1,0] # _complement[0] == 1 and _complement[1] == 0
    for i in range(len(l)):
        yield (l[:i] + [_complements[l[i]]] + l[i+1:])
