"""
Functions to introduce Arguments into Debates and update Positions accordingly.
""" 

from itertools import combinations, chain
from copy import deepcopy
from random import randrange, choice
from sympy import And, Not
from taupy import (Argument, Debate, satisfiability, satisfiability_count, 
                   dict_to_prop, next_neighbours)

import taupy.simulation.strategies as strategies    

def introduce(_sim, source=None, target=None, strategy=None):
    """
    Introduce an argument following an argumentation strategy from source to
    target. If source or target are unspecified, they are filled in 
    automatically. The source and target should be given as integers representing
    the position's location in the Simulation.positions collection.

    ----
    References:
    [1] Betz, Gregor. 2012. Debate dynamics: How controversy improves our beliefs. P. 94, Table 6.1            
    """
    # Check if the simulation has possible premise combinations left
    if len(_sim.premisepool) == 0:
        _sim.log.append("Introducing an argument failed because the Simulation's premise pool is depleted.")
        return False

    # First check which positions have to be allocated (if any)
    if strategy["source"] | strategy["target"]:
        # Only copy the list if needed.
        positions = _sim.positions[-1].copy()
        if strategy["source"]:
            if source:
                positions.remove(source)
                source_pos = source
            else:
                source_pos = positions.pop(randrange(0,len(positions)))
        if strategy["target"]:
            if target:
                positions.remove(target)
                target_pos = target
            else:
                target_pos = positions.pop(randrange(0,len(positions)))
    
    # Track if source and target positions have been set. This is send to log later.
    if not strategy["source"]:
        source_pos = None
    if not strategy["target"]:
        target_pos = None
    
    while True:
        available_premises = _sim.premisepool.copy()

        if strategy["pick_premises_from"] == None:
            selected_premises = available_premises.pop(randrange(0,len(available_premises)))
            _found_premises = True
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

            possible_premises = possible_premises & set(available_premises)

            if len(possible_premises) == 0:
                # There are no further available premises. 
                _found_valid_argument = False
                break
            else:
                selected_premises = choice(list(possible_premises))
                available_premises.remove(selected_premises)
                _found_premises = True

        if _found_premises:
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
            if len(possible_conclusions) == 0:
                _sim.log.append("Introducing argument failed because no matching conclusion could be found for the selected premises. %d combinations of premises remain." % (len(available_premises)) )
            else:
                selected_conclusion = choice(possible_conclusions)

                if len(_sim) == 0 or satisfiability(And( _sim[-1], Argument(And(*selected_premises), selected_conclusion))):
                    _sim.premisepool.remove(selected_premises)
                    _found_valid_argument = True
                    break
                else:
                    _sim.log.append("Introducing argument failed because of UNSAT. %d combinations of premises remain." % (len(available_premises)) )
                    if len(available_premises) == 0:
                        _found_valid_argument = False
                        break
    
    if _found_valid_argument:
        _sim.log.append("Introduce argument with strategy '%s'. Premises: %s. Conclusion: %s. Source: %s. Target: %s." % (strategy["name"], And(*selected_premises), selected_conclusion, source_pos, target_pos))
        
        if len(_sim) == 0:
            # Initialise the Simulation with _argument
            _sim.append(Debate(Argument(And(*selected_premises), selected_conclusion)))
        else:
            if type(_sim[-1]) == Argument: 
                # If a Debate conists of just one Argument, the debate's type
                # is changed to Argument b/c of inheritance from sympy cls.
                _sim.append(Debate( _sim[-1], Argument(And(*selected_premises), selected_conclusion)))
            else: 
                # Assuming type is Debate or And
                _sim.append(Debate( *_sim[-1].args, Argument(And(*selected_premises), selected_conclusion)))
        
        return True
        # return Argument(And(*selected_premises), selected_conclusion)    
    else:
        _sim.log.append("Introduction of with strategy '%s' failed. No valid combinations left in the premise pool." % (strategy["name"]) )
        return False

def response(_sim, method):
    """
    Updating Positions in a debate. This needs more work!
    """
    
    if method == "random":
        updated_positions = []
        for p in _sim.positions[-1]:
            if satisfiability(And(dict_to_prop(p), _sim[-1])):
                updated_positions.append(p)
            else:
                u = deepcopy(p)
                u |= choice(satisfiability(And(*_sim.sentencepool, _sim[-1]),all_models=True)) 
                updated_positions.append(u)
        _sim.positions.append(updated_positions)        
    
    if method == "closest_coherent":
        updated_positions = []
        for p in _sim.positions[-1]:
            if satisfiability(And(dict_to_prop(p), _sim[-1])):
                updated_positions.append(p)
                _sim.log.append("Position with index %d did not need an update." % (_sim.positions[-1].index(p)))
            else:
                u = deepcopy(p)
                u |= choice(next_neighbours(p, _sim[-1]))
                updated_positions.append(u)
                _sim.log.append("Position with index %d was updated with strategy closest_coherent." % (_sim.positions[-1].index(p)))
        _sim.positions.append(updated_positions)