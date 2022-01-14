from taupy.basic.utilities import satisfiability, dict_to_prop
from sympy.logic.algorithms.dpll2 import dpll_satisfiable
from taupy.basic.core import Debate, Argument
from copy import deepcopy
from sympy import And, Not

class Position(dict):
    """
    A position in terms of the theory of dialectical structure, used to model
    agent's belief systems. 
    """
    def __init__(self, debate, *args, introduction_strategy=None, update_strategy=None):
        self.debate = debate
        self.introduction_strategy = introduction_strategy
        self.update_strategy = update_strategy
        dict.__init__(self, *args)
        
    def is_complete(self):
        return True if self.keys() == self.debate.atoms() else False
    
    def is_coherent(self):
        return satisfiability(And(dict_to_prop(self), self.debate))
    
    def is_closed(self):
        # For backwards compatibility, this class method links to a function
        # which was introduced later.
        return closedness(self)

    def inverse(self):
        """
        Return the inverse of a position, that is the position that assigns 
        contradictory truth values.
        """
        return {k: not self[k] for k in self}   

def position_compatibility(pos1, pos2, deep=False):
    """
    Check for compatibility of pos1 and pos2. When deep=False, the check is 
    only lexicographic. A deep check also checks for satisfiability of the 
    intersected positions.
    """
    if deep == True and pos1.debate != pos2.debate:
        raise ValueError("Deep compatibility can only be checked for positions \
            of the same debate.")
    
    if any(pos1[k] in pos2 and pos1[k] != pos2[k] for k in pos1):
        return False
    else:
        if deep == True:
            if not satisfiability(And(dict_to_prop({**pos1, **pos2})), 
                                  pos1.debate):
                return False
            else:
                return True
        else:
            return True

def closedness(pos, debate=None, return_alternative=False):
    """
    A position `pos` is closed relative to a debate when it follows its dialectical
    obligations: if a position assigns True to all of the premises of an argument
    in the debate, it must also assign True to the conclusion of that argument.

    This function is not embedded as a method for the Position class so that it
    can be applied to Position-like objects like dicts. 

    Returns a Boolean by default indicating the closedness status of `pos`. However,
    if `return_alternative` is `True`, the function will return a tuple containing
    the closedness value and an alternative. If the position is closed, the alternative
    will be the position itself, but in case of closeness violation, the function 
    will close the position and return this alternative. If a position is not closed, 
    there is exactly one alternative that is.
    """
    if debate == None:
        # Assume that the position is a Position object and use its associated
        # debate.
        d = pos.debate
    else:
        # The user gave a specific debate with respect to which closedness is
        # analysed.
        d = debate
    
    position = deepcopy(pos)
    suspended = [k for k in position if position[k] == None]

    # Defaulting to True here means that closedness is confirmed if the position
    # does not suspend on any sentence.
    if dpll_satisfiable(And(dict_to_prop(position), d)):
        closedness_status = True
    else:
        closedness_status = False
        print("taupy Warning: Incoherence in input, closedness undefined.")

    for s in suspended:
        sat_status_t = dpll_satisfiable(And(dict_to_prop(position), d, s))
        sat_status_f = dpll_satisfiable(And(dict_to_prop(position), d, Not(s)))
        
        if not (sat_status_t and sat_status_f):
            if sat_status_t and not sat_status_f:
                position[s] = True
                closedness_status = False
            if not sat_status_t and sat_status_f:
                position[s] = False
                closedness_status = False                    

    return (closedness_status, position) if return_alternative else closedness_status