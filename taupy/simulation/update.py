"""
Functions to introduce Arguments into Debates and update Positions accordingly.
""" 

from itertools import combinations, chain
from copy import deepcopy
import numpy as np
from random import randrange, choice
from sympy import And, Not
from sympy.logic.algorithms.dpll2 import dpll_satisfiable
from taupy import (Argument, Debate, Position, satisfiability, satisfiability_count, 
                   dict_to_prop, next_neighbours, hamming_distance, switch_deletion_neighbourhood)

import taupy.simulation.strategies as strategies

def introduce(_sim, source=None, target=None, strategy=None):
    """
    Introduce an argument following an argumentation strategy from ``source`` to
    ``target``. If ``source`` or ``target`` are unspecified, they are filled in 
    automatically. The ``source`` and ``target`` should be given as integers 
    representing the position's location in the ``Simulation.positions`` 
    collection.
    """
    # Check if the simulation has possible premise combinations left
    if len(_sim.premisepool) == 0:
        _sim.log.append("Introducing an argument failed because the \
            Simulation's premise pool is depleted.")
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
    
    # Track if source and target positions are set and store for log entry.
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
                    possible_premises = set(chain(*map(lambda i: combinations(dict_to_prop(target_pos).args, i), _sim.argumentlength)))
                except TypeError: # the input r is not an iterable. Now assume integer.
                    possible_premises = set(combinations(dict_to_prop(target_pos).args, r=_sim.argumentlength))

            possible_premises = possible_premises & set(available_premises)

            if len(possible_premises) == 0:
                # There are no further available premises.
                _sim.log.append("Can't find premises for source %s and target %s" % (source_pos, target_pos))
                _found_valid_argument = False
                break
            else:
                selected_premises = choice(list(possible_premises))
                available_premises.remove(selected_premises)
                _found_premises = True

        if _found_premises:
            # Get the conclusion candidates from the sentence pool
            possible_conclusions = list(set(_sim.sentencepool) - set(_sim.leaves) - set(And(*selected_premises).atoms()))
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
                _sim.premisepool.remove(selected_premises)
            else:
                selected_conclusion = choice(possible_conclusions)

                if satisfiability(And( _sim[-1], Argument(And(*selected_premises), selected_conclusion))):
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
        
        if len(_sim) == 1:
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
        _sim.log.append("Introduction with strategy '%s' failed. No valid combinations left in the premise pool." % (strategy["name"]) )
        return False

def response(_sim, method):
    """
    Updating Positions in a debate.
    
    Currently, we only have one sensisble strategy, ``closest_coherent``. 
    Surely, many more remain to be discovered.
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
    
    if method == "closest_coherent_complete_search":
        updated_positions = []
        models = list(satisfiability(_sim[-1], all_models="True"))
        examinees = [{k: i[k] for k in i if k in _sim[-1].atoms()} for i in _sim.positions[-1]]
        distances = np.array([[hamming_distance(i, j) for i in models] for j in examinees])

        for i in range(distances.shape[0]):
            if np.min(distances[i]) == 0:
                updated_positions.append(_sim.positions[-1][i])
                _sim.log.append("Position with index %d did not need an update." % (i))
            else:
                u = deepcopy(_sim.positions[-1][i])
                update_index = choice(np.where(distances[i] == distances[i].min())[0].tolist())
                u |= models[update_index]
                updated_positions.append(u)
                _sim.log.append("Position with index %d was updated with strategy closest_coherent." % (i))

        _sim.positions.append(updated_positions)

    if method == "closest_coherent":
        updated_positions = []
        list_of_models = list(satisfiability(_sim[-1], all_models=True))
        for p in _sim.positions[-1]:
            if dpll_satisfiable(And(dict_to_prop(p), _sim[-1])):
                updated_positions.append(p)
                _sim.log.append("Position with index %d did not need an update." % (_sim.positions[-1].index(p)))
            else:
                u = deepcopy(p)
                u |= choice(next_neighbours(p, debate=_sim[-1], models=list_of_models))
                updated_positions.append(u)
                _sim.log.append("Position with index %d was updated with strategy closest_coherent." % (_sim.positions[-1].index(p)))
        _sim.positions.append(updated_positions)

    if method == "closest_closed_partial_coherent":
        """
        This is a "poor man's Levenshtein automaton": we are looking for all positions with a given
        edit distance to the positions that need updating, and we then select the one with the least
        distance to the original position.
        """
        updated_positions = []
        
        for position in _sim.positions[-1]:
            
            # First, let's see whether the position has any chance wrt the updated debate:
            if dpll_satisfiable(And(dict_to_prop(position), _sim[-1])):
                new_position = deepcopy(position)
                _sim.log.append("Position with index %d is still coherent given the new debate." % (_sim.positions[-1].index(position)))
            else:
                # The position needs other updates than for closure.
                for d in range(len(position)):
                    # Let's first build the list of candidates
                    candidates = [{**{k: position[k] for k in position if k not in i[0]}, 
                                  **{k: not position[k] for k in i[1]}} for i in switch_deletion_neighbourhood(position, d)]
                    # We're explicitly sorting that list. The sorting here is crucial for 
                    # agent's behaviour. They are assumed to start with the longest candidates,
                    # i.e. they're trying to have as many TVAs as possible.

                    candidates.sort(key=len, reverse=True)

                    for c in candidates:
                        if dpll_satisfiable(And(dict_to_prop(c), _sim[-1])):
                            new_position = deepcopy(position)
                            new_position.clear()
                            new_position |= c
                            _sim.log.append("Found a near neighbour for position at index %d which is coherent." % (_sim.positions[-1].index(position)))
                            break
                    else:
                        _sim.log.append("Did not find any replacement for the position at index %d. I sense something is afoot." % (_sim.positions[-1].index(position)))

            # Now that we have found a coherent version of the Position, let's check for closedness.
            if len(_sim) > 2:
                for argument in _sim[-1].args:
                    # For each argument, check if all premises are accepted.
                    if all (premise in new_position and new_position[premise] == True for premise in argument.args[0].args):
                        # Then make sure the conclusion is accepted as well.
                        if argument.args[1] not in new_position:
                            _sim.log.append("Position needs update due to not being closed.") 
                            new_position[argument.args[1]] = True
            else:
                # The first debate stage of a Simulation needs different treatment, because the content then
                # is an Argument, not a Debate.
                if all (premise in new_position and new_position[premise] == True for premise in _sim[-1].args[0].args):
                        # Then make sure the conclusion is accepted as well.
                        if _sim[-1].args[1] not in new_position:
                            _sim.log.append("Position needs update due to not being closed.") 
                            new_position[_sim[-1].args[1]] = True

            # A final check whether the new position is satisfiable.
            if dpll_satisfiable(And(dict_to_prop(new_position), _sim[-1])):
                    updated_positions.append(new_position)
        
        _sim.positions.append(updated_positions)