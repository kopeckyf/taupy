from taupy.basic.utilities import satisfiability, dict_to_prop
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
    will close the position and return this alternative. 

    (Note that finding the alternative is deterministic, i.e. there is a unique closed
    alternative for a non-closed position.)
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
    # Let's default to a position being closed, unless we spot a violation. The code
    # below loops through the arguments of the debate to spot whether there is a
    # closedness violation. Otherwise, it says the position is closed.
    closedness_status = True

    # We need to do type checking here, unfortunately, because a Debate with a single
    # Argument reduces to an Argument object (owing to the underlying implementation).
    # This type check will become obsolete in a future release.
    if isinstance(d, Debate):
        for argument in d.args:
            # For each argument, check if all premises are accepted.
            if all (premise in position and position[premise] == True for \
                premise in argument.args[0].atoms() if premise in argument.args[0].args) and \
                    all (premise in position and position[premise] == False for \
                        premise in argument.args[0].atoms() if Not(premise) in argument.args[0].args):
                            # Then make sure the conclusion is accepted as well.
                            conclusion, = argument.args[1].atoms()
                            if conclusion not in position:
                                closedness_status = False
                                if return_alternative:
                                    position[conclusion] = False if Not(conclusion) in argument.args else True
                                
    if isinstance(d, Argument):
        # The first debate stage of a Simulation needs different treatment, because the content then
        # is an Argument, not a Debate.
        if all (premise in position and position[premise] == True \
            for premise in d.args[0].atoms() if premise in d.args[0].args) and \
                all (premise in position and position[premise] == False \
                    for premise in d.args[0].atoms() if Not(premise) in d.args[0].args):
                        # Then make sure the conclusion is accepted as well.
                        conclusion, = d.args[1].atoms()
                        if conclusion not in position:
                            closedness_status = False
                            if return_alternative:
                                position[conclusion] = False if Not(conclusion) in d.args else True
    
    return (closedness_status, position) if return_alternative else closedness_status