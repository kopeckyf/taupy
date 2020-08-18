from taupy.basic.utilities import satisfiability_count, dict_to_prop
from sympy.logic import (And, Implies, Not)
from fractions import Fraction

def doj( pos, debate=None, conditional=None ):
    """
    Degree of justification for a position given its associated debate.
    """
    
    if debate is None: 
        # Defaulting to the debate attribute of pos
        debate = pos.debate
    
    if conditional is not None:
        if pos.debate is not conditional.debate:
            raise ValueError("Positions do not belong to same debate")
        # Adding the condition to the inspected debate.
        debate = And(dict_to_prop(conditional), debate)
    
    _n = satisfiability_count ( And(dict_to_prop(pos), debate) )
    _m = satisfiability_count ( debate )
    return Fraction(_n, _m)
