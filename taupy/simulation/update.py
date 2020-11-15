"""
Functions to introduce Arguments into Debates and update Positions accordingly.
""" 

from itertools import combinations, chain
from random import randrange, choice
from sympy import And, Not
from taupy import (Argument, Debate, satisfiability, satisfiability_count, 
                   dict_to_prop, next_neighbours)

import taupy.simulation.strategies as strategies

def debug_strategies():
    print (strategies.attack)

def introduce(_simulation, _argument):
    """
    Introduce an Argument to a Simulation.
    """
    
    if len(_simulation) == 0:
        # Initialise the Simulation with _argument
        _simulation.append(Debate(_argument))
    else:
        if satisfiability( And( _simulation[-1], _argument ) ):
            if type(_simulation[-1]) == Argument: 
                # If a Debate conists of just one Argument, the debate's type
                # is changed to Argument b/c of inheritance from sympy cls.
                _simulation.append(Debate( _simulation[-1], _argument ))
            else: 
                # Assuming type is Debate or And
                _simulation.append(Debate( *_simulation[-1].args, _argument ))
        else:
            print("unsat")
    
#    try:
#        _simulation.premisepool.remove(_argument.args[0].args)
#    except ValueError:
#        print("Introduction unsuccesful b/c premises not available.")
    
def response(_simulation, method, _stage1=None, _stage2=None):
    """
    Updating Positions in a debate.
    """
    
    if _stage1 == None:
        _stage1 = _simulation[-1]
        
    if _stage2 == None:
        _stage2 = _simulation[-2]

def introduce_strategical(_sim, source=None, target=None, strategy=None):
    """
    Introduce an argument following an argumentation theory from source to
    target. If source or target are unspecified, they are filled in 
    automatically. The source and target should be given as integers representing
    the position's location in the Simulation.positions collection.

    ----
    References:
    [1] Betz, Gregor. 2012. Debate dynamics: How controversy improves our beliefs. P. 94, Table 6.1            
    """
    # First check which positions have to be allocated (if any)
    if strategy["source"] | strategy["target"]:
        # Only copy the list if needed.
        positions = _sim.positions[-1].copy()
        if strategy["source"]:
            source_pos = positions.pop(source) if source else positions.pop(randrange(0,len(positions)))
        if strategy["target"]:
            target_pos = positions.pop(target) if target else positions.pop(randrange(0,len(positions)))
    
    # Track if source and target positions have been set. This is send to log later.
    if not strategy["source"]:
        source_pos = None
    if not strategy["target"]:
        target_pos = None
    
    if strategy["pick_premises_from"] == None:
        selected_premises = _sim.premisepool.pop(randrange(0,len(_sim.premisepool)))
    else:
        if strategy["pick_premises_from"] == "source":
            try: # Assume variable length of subsequence. Following an idea by Dan H.
                possible_premises = set(chain(*map(lambda i: combinations(dict_to_prop(source_pos).args, i), _sim.argumentlength)))
            except TypeError: # the input r is not an iterable. Now assume integer.
                possible_premises = set(combinations(dict_to_prop(source_pos).args, r=_sim.argumentlength))
        
        if strategy["pick_premises_from"] == "target":
            try: # Assume variable length of subsequence. Following an idea by Dan H.
                possible_premises = set(chain(*map(lambda i: combinations(target_pos, i), _sim.argumentlength)))
            except TypeError: # the input r is not an iterable. Now assume integer.
                possible_premises = set(combinations(dict_to_prop(target_pos).args, r=_sim.argumentlength))

        possible_premises = possible_premises & set(_sim.premisepool)
        selected_premises = choice(list(possible_premises))
        _sim.premisepool.remove(selected_premises)

    # Get the conclusion candidates from the sentence pool
    possible_conclusions = list(set(_sim.sentencepool) - set(And(*selected_premises).atoms()))
    possible_conclusions += list(Not(i) for i in possible_conclusions)

    # Directed strategies act as filters on possible conclusions. The list of possible values is not exhausted b/c it is not required by the currently known strategies.
    if strategy["source_accepts_conclusion"] == "Yes":
        possible_conclusions = list(set(possible_conclusions) & set(dict_to_prop(source_pos).args))

    if strategy["source_accepts_conclusion"] == "Toleration":
        possible_conclusions = list(set(possible_conclusions) - {Not(i) for i in dict_to_prop(source_pos).args})
        
    if strategy["target_accepts_conclusion"] == "No":
        possible_conclusions = list(set(possible_conclusions) & set([Not(i) for i in dict_to_prop(target_pos).args]))
    
    # Now select a conclusion from the (un-)filtered list of conclusions:
    selected_conclusion = choice(possible_conclusions)

    _sim.log.append("Introduce argument with strategy '%s'. Premises: %s. Conclusion: %s. Source: %s. Target: %s." % (strategy["name"], And(*selected_premises), selected_conclusion, source_pos, target_pos))

    return Argument(And(*selected_premises), selected_conclusion)    
    
def response_random(_sim):
    """
    
    """
    _updated = []
    for p in _sim.positions[-1]:
        if satisfiability(And(dict_to_prop(p), _sim[-1])):
            _updated.append(p)
        else:
            _updated.append(choice(satisfiability(And(*_sim.sentencepool, _sim[-1]),all_models=True)))
    _sim.positions.append(_updated)

def closest_coherent(_sim):
    """
    
    """
    _updated = []
    for p in _sim.positions[-1]:
        if satisfiability(And(dict_to_prop(p), _sim[-1])):
            _updated.append(p)
            print ("no update needed")
        else:
            _updated.append({**p, **choice(next_neighbours(p,_sim[-1]))})
            print ("update needed")
    _sim.positions.append(_updated)
