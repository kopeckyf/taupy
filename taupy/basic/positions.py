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

        Judgement suspension is not inverted.
        """
        return {**{k: not self[k] for k in self if self[k] != None},
                **{k: None for k in self if self[k] == None}}

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

    This function assumes that the input `pos` is coherent. If in doubt, you should
    perform a coherence check first. Incoherent positions *can* be labelled as closed
    by this algorithm, although this is nonsensical.

    Returns a Boolean by default indicating the closedness status of `pos`. However,
    if `return_alternative` is `True`, the function will return a tuple containing
    the closedness value and an alternative. The alternative is obtained by checking if
    the position follows entailment. If the position is closed, the alternative
    will be the position itself, but in case of closeness violation, the function 
    will close the position by filling up the position via entailment.

    A shortcut of this function exists under `Position.is_closed()`. 
    """
    if debate == None:
        # Assume that the position is a Position object.
        d = pos.debate
    else:
        # The user gave a specific debate.
        d = debate
    
    position = deepcopy(pos)
    ignorant = {a for a in d.atoms() if a not in position} 
    suspended = {k for k in position if position[k] == None}
    
    # Defaulting to True here means that closedness is confirmed if the position
    # does not suspend on any sentence and isn't ignorant of any.
    closedness_status = True

    for s in ignorant | suspended:
        sat_assume_true = dpll_satisfiable(And(dict_to_prop(position), d, s))
        sat_assume_false = dpll_satisfiable(And(dict_to_prop(position), d, Not(s)))
        
        # Does the position depend on the proposition for closedness?
        if not (sat_assume_true and sat_assume_false):
            # Case 1: The position depends on the truth of s for closedness.
            if sat_assume_true and not sat_assume_false:
                position[s] = True
                closedness_status = False
            # Case 2: The position depends on the falsehood of s.
            if not sat_assume_true and sat_assume_false:
                position[s] = False
                closedness_status = False

        # If the closedness status is settled after current s and no alternative 
        # is requested, stop the search early to save some computation time.
        # If an alternative is requested, we need to check all propositions.
        if not return_alternative and closedness_status == False:
            break                    

    return (closedness_status, position) if return_alternative else closedness_status