from sympy import And

from taupy.basic.utilities import satisfiability, dict_to_prop

class Position(dict):
    """
    Document me! 
    """
    def __init__(self, debate, *args):
        self.debate = debate
        dict.__init__(self, *args)
        
    def is_complete(self):
        return True if self.keys() == self.debate.atoms() else False
    
    def is_coherent(self):    
        return True if satisfiability(And(dict_to_prop(self), self.debate)) else False
    
    def is_closed(self):
        for argument in self.debate.args:
            if all ( premise in self and self[premise] is True for premise in argument.args[0].args ):
                if argument.args[1] not in self or self[ argument.args[1] ] is False:
                    return False
        else:
            return True
