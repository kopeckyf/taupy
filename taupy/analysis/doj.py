from taupy.basic.utilities import satisfiability_count, dict_to_prop
from sympy.logic import And
from fractions import Fraction

def doj(pos, debate=None, conditional=None):
    """
    Returns the degree of justification for the position in ``pos`` relative
    to a ``debate``, as defined in [Betz2012]_. If ``debate`` is `None`, the 
    debate stored in the Position object is used. 
    
    The *conditional* doj is returned if ``conditional`` is given another
    position of the same debate. When ``conditional`` is set, ``debate``
    must be `None`.
    """
    
    if debate is None: 
        # Defaulting to the debate attribute of pos
        debate = pos.debate
    
    if conditional is not None:
        if pos.debate != conditional.debate:
            raise ValueError("Positions do not belong to same debate")
        # Adding the condition to the inspected debate.
        debate = And(dict_to_prop(conditional), debate)
    
    n = satisfiability_count(And(dict_to_prop(pos), debate))
    m = satisfiability_count(debate)
    return Fraction(n, m)
