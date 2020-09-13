"""
Functions to introduce Arguments into Debates and update Positions accordingly.
""" 

from random import randrange, choice
from sympy import And, Not
from taupy import Argument, Debate, satisfiability, satisfiability_count
from .simulation import Simulation

def introduce(_simulation, _argument):
    """
    Introduce an Argument to a Simulation.
    """
    
    if len(_simulation) == 0:
        # Initialise the Simulation with _argument
        _simulation.append(Debate(_argument))
    else:
        print ( And(_simulation[-1], _argument ) )
        print ( satisfiability_count ( And(_simulation[-1], _argument ) ) )
        if satisfiability( And( _simulation[-1], _argument ) ):
            if type(_simulation[-1]) == Argument:
                _simulation.append(Debate( _simulation[-1], _argument ))
            else:
                _simulation.append(Debate( *_simulation[-1].args, _argument ))
        else:
            print("unsat")
    
    try:
        _simulation.premisepool.remove(_argument.args[0].args)
    except ValueError:
        print("Introduction unsuccesful b/c premises not available.")
    
def response(tau1, tau2, method):
    """
    Updating Positions in a debate.
    """    
    pass


def random(_sim):
    _premises = _sim.premisepool.pop(randrange(0,len(_sim.premisepool)))
    _possible_conclusions = list ( set(_sim.sentencepool) - set(And(*_premises).atoms()) )
    _possible_conclusions += list(Not(i) for i in _possible_conclusions)
    _conclusion = choice(_possible_conclusions)
    return Argument( And(*_premises), _conclusion)
