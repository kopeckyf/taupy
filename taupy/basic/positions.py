from sympy import And, Not
from taupy.basic.utilities import satisfiability, dict_to_prop

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
        """
        ⚠️ Work in progress ⚠️
        Warning: This implementation does not check for coherence. It can label incoherent positions as closed!
        It currently only works for debates with more than 1 argument.
        """
        for argument in self.debate.args:
            if all (premise in self and self[premise] == True for premise in argument.args[0].atoms() if \
                premise in argument.args[0].args) and all (premise in self and self[premise] == False for \
                    premise in argument.args[0].atoms() if Not(premise) in argument.args[0].args):
                        conclusion, = argument.args[1].atoms()
                        if conclusion not in self:
                            return False
        else:
            return True

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
