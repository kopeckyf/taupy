"""
Functions to introduce Arguments into Debates and update Positions accordingly.
"""

from itertools import combinations
from copy import deepcopy
import numpy as np
from random import randrange, choice
from sympy import And, Not
from sympy.logic.algorithms.dpll2 import dpll_satisfiable
from taupy import (Argument, Debate, Position, satisfiability, dict_to_prop, next_neighbours,
                   hamming_distance, satisfiable_neighbours, edit_distance, fetch_premises)
import taupy.simulation.strategies as strategies

def introduce(_sim, source=None, target=None, strategy=None):
    """
    Introduce an argument following an argumentation strategy from ``source`` to
    ``target``. If ``source`` or ``target`` are unspecified, they are filled in
    automatically. The ``source`` and ``target`` should be given as integers
    representing the position's location in the ``Simulation.positions``
    collection.
    """

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

    seen_premises = []

    while True:

        if strategy["pick_premises_from"] == None:
            selected_premises = fetch_premises(_sim.premise_candidates(),
                                               length=_sim.argumentlength,
                                               exclude=_sim.used_premises + seen_premises)
            if selected_premises:
                _found_premises = True
        else:
            if strategy["pick_premises_from"] == "source":
                selected_premises = fetch_premises(set(dict_to_prop(source_pos).args),
                                                   length=_sim.argumentlength,
                                                   exclude=_sim.used_premises + seen_premises)

            if strategy["pick_premises_from"] == "target":
                selected_premises = fetch_premises(set(dict_to_prop(target_pos).args),
                                                   length=_sim.argumentlength,
                                                   exclude=_sim.used_premises + seen_premises)

            if selected_premises:
                _found_premises = True
                seen_premises.append(selected_premises)
            else:
                # Can't find available premises.
                _sim.log.append("Can't find premises for source %s and target %s" % (source_pos, target_pos))
                _found_valid_argument = False
                break

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
                _sim.log.append("Introducing argument failed because no matching conclusion could be found for the selected premises. %d combinations of premises have been tried." % (len(seen_premises)))
                _sim.used_premises.append(selected_premises)
            else:
                selected_conclusion = choice(possible_conclusions)

                if satisfiability(And( _sim[-1], Argument(And(*selected_premises), selected_conclusion))):
                    _sim.used_premises.append(selected_premises)
                    _found_valid_argument = True
                    break
                else:
                    _sim.log.append("Introducing argument failed because of UNSAT. %d combinations of premises tried." % (len(seen_premises)) )
                    if not selected_premises:
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
                new_position = Position(_sim[-1],
                                        position,
                                        introduction_strategy=position.introduction_strategy,
                                        update_strategy=position.update_strategy)
                _sim.log.append("Position with index %d is still coherent given the new debate." % (_sim.positions[-1].index(position)))
            else:
                # The position needs other updates than for closure.
                # Thank you, @thefourtheye
                l = list({frozenset(model.items()):model for model in \
                    [{j: i[j] for j in i if j in position} for i in \
                        satisfiable_neighbours(_sim[-1], position)]}.values())

                k = len(position)
                while True:
                    r = list({frozenset(model.items()):model for model in \
                        [item for sublist in [[{i:j[i] for i in x} for x in \
                            combinations(j, k)] for j in l] for item in sublist]}.values())

                    a = np.array([edit_distance(i, position) for i in r])

                    if a.size > 0:
                        new_position = Position(_sim[-1],
                                        r[choice(np.argwhere(a == np.amin(a)).flatten().tolist())],
                                        introduction_strategy=position.introduction_strategy,
                                        update_strategy=position.update_strategy)

                        break
                    else:
                        k -= 1

                _sim.log.append("Position with index %d updated to a new position, edit distance %d." % (_sim.positions[-1].index(position), edit_distance(position, new_position)))

            # Now that we have found a coherent version of the Position, let's check for closedness.
            if len(_sim[-1].args) > 0:
                # Only check closedness if the Simulation contains Arguments.
                if isinstance(_sim[-1], Debate):
                    for argument in _sim[-1].args:
                        # For each argument, check if all premises are accepted.
                        if all (premise in new_position and new_position[premise] == True for \
                            premise in argument.args[0].atoms() if premise in argument.args[0].args) and \
                                all (premise in new_position and new_position[premise] == False for \
                                    premise in argument.args[0].atoms() if Not(premise) in argument.args[0].args):
                                        # Then make sure the conclusion is accepted as well.
                                        conclusion, = argument.args[1].atoms()
                                        if conclusion not in new_position:
                                            _sim.log.append("Position needs update due to not being closed.")
                                            new_position[conclusion] = False if Not(conclusion) in argument.args else True
                if isinstance(_sim[-1], Argument):
                    # The first debate stage of a Simulation needs different treatment, because the content then
                    # is an Argument, not a Debate.
                    if all (premise in new_position and new_position[premise] == True \
                        for premise in _sim[-1].args[0].atoms() if premise in _sim[-1].args[0].args) and \
                            all (premise in new_position and new_position[premise] == False \
                                for premise in _sim[-1].args[0].atoms() if Not(premise) in _sim[-1].args[0].args):
                                    # Then make sure the conclusion is accepted as well.
                                    conclusion, = _sim[-1].args[1].atoms()
                                    if conclusion not in new_position:
                                        _sim.log.append("Position needs update due to not being closed.")
                                        new_position[conclusion] = False if Not(conclusion) in _sim[-1].args else \
                                            True

            # A final check whether the new position is satisfiable.
            if dpll_satisfiable(And(dict_to_prop(new_position), _sim[-1])):
                    updated_positions.append(new_position)

        _sim.positions.append(updated_positions)
