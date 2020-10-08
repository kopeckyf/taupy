"""
Functions to introduce Arguments into Debates and update Positions accordingly.
""" 

from random import randrange, choice
from sympy import And, Not
from taupy import (Argument, Debate, satisfiability, satisfiability_count, 
                   dict_to_prop, next_neighbours)
from .simulation import Simulation

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

def introduce_random(_sim):
    _premises = _sim.premisepool.pop(randrange(0,len(_sim.premisepool)))
    _possible_conclusions = list(set(_sim.sentencepool) - set(And(*_premises).atoms()))
    _possible_conclusions += list(Not(i) for i in _possible_conclusions)
    _conclusion = choice(_possible_conclusions)
    return Argument( And(*_premises), _conclusion)

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
            # Python < 3.7
            #_closest = p.copy()
            #_closest.update(...)
            # Python >= 3.7
            _updated.append({**p, **choice(next_neighbours(p,_sim[-1]))})
            print ("update needed")
    _sim.positions.append(_updated)
