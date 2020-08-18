def doj( pos, debate=None, conditional=None ):
    """
    Degree of justification for a position p given its associated debate.
    
    """
    _m = 0; _n = 0
    
    if debate is None: 
        # Defaulting to the debate attribute of pos
        debate = pos.debate
    
    if conditional is not None:
        if pos.debate is not conditional.debate:
            raise ValueError("Positions do not belong to same debate")
        # Adding the condition to the inspected debate.
        debate = And(dict_to_prop(conditional), debate)
    
    for position in satisfiable( debate, all_models = True ):
        if position:
            _m += 1
            if pos.items() <= position.items():
                _n += 1
    return Fraction(_n, _m)
