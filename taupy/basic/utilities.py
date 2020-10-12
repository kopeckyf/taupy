from dd.autoref import BDD
from sympy.logic import to_cnf, And, Implies, Not
from sympy import symbols

def dict_to_prop(dictionary):
    """
    Helper function that converts a dictionary to a propositional formula, 
    acknowledging dictionary's truth-value attributions.
    """
    _l = []
    for (k, v) in dictionary.items():
        if v: _l.append(k)
        if not v: _l.append(Not(k))
    return And(*_l)

def iter_to_string(l, sep=""):
    """
    Helper function that converts a dictionary position to a bit string.
    """
    return sep.join(str(i) for i in l)

def iter_to_list_of_strings(l):
    return [str(i) for i in l]

def neighbours_of_list(l):
    """
    Find the neighbours of a position in list format. A neighbour is a position
    that has HD = 1 to the position in question.
    """
    _complements = [1,0] # _complement[0] == 1 and _complement[1] == 0
    for i in range(len(l)):
        yield (l[:i] + [_complements[l[i]]] + l[i+1:])
        
def satisfiability_count(_formula):
    """
    Count the models that satisfy a Boolean formula, using Binary decision diagrams. 
    """
    _variables = iter_to_list_of_strings(_formula.atoms())
    _diagram = BDD()
    _diagram.declare(*_variables)
    _expression = _diagram.add_expr(str(to_cnf(_formula)))
    return _diagram.count(_expression, nvars=len(_formula.atoms()))

def satisfiability(_formula, all_models = False):
    """
    Return a generator of models for the given Boolean formula, using BDDs
    """
    _variables = iter_to_list_of_strings(_formula.atoms())
    _diagram = BDD()
    _diagram.declare(*_variables)
    
    if all_models:
        _expression = _diagram.add_expr(str(to_cnf(_formula)))
        return [{symbols(k): v for (k, v) in m.items()} for m in \
            _diagram.pick_iter(_expression, care_vars={str(i) for i in \
                _formula.atoms()})]
    else:
        try:
            _expression = _diagram.add_expr(str(to_cnf(_formula)))
            next(_diagram.pick_iter(_expression))
            return True
        except StopIteration:
            return False
