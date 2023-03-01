"""
Functions to introduce Arguments into Debates and update Positions accordingly.
"""

from copy import deepcopy
import numpy as np
from more_itertools import powerset, unique_everseen
from random import randrange, choice, choices, shuffle
from sympy import And, Not, symbols
from sympy.logic.algorithms.dpll2 import dpll_satisfiable
from taupy import (Argument, Debate, EmptyDebate, Position, satisfiability, closedness, 
                   dict_to_prop, next_neighbours,
                   hamming_distance, edit_distance, fetch_conclusion, select_premises,
                   proposition_levels_from_debate,
                   z3_assertion_from_argument, z3_soft_constraints_from_position, 
                   z3_all_models)
import taupy.simulation.strategies as strategies
import z3

def introduce(_sim, source=None, target=None, strategy=None):
    """
    Introduce an argument following an argumentation strategy from ``source`` to
    ``target``. If ``source`` or ``target`` are unspecified, they are filled in
    automatically. The ``source`` and ``target`` should be given as integers
    representing the position's location in the ``Simulation.positions``
    collection.
    """

    # We begin by determining source and target positions,
    # but only if the introduction strategy requires them.
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

    # Track if source and target positions are set.
    if not strategy["source"]:
        source_pos = None
    if not strategy["target"]:
        target_pos = None

    # Now we are looping over all available premises, and we store the ones already tried.
    seen_premises = []

    while True:
        # There are two methods to grow the debate: one generates a random graph, the other one
        # a tree structure. 
        if _sim.debate_growth == "random":
            selected_premises = select_premises(sentencepool=_sim.premise_candidates(),
                                                length=_sim.argumentlength,
                                                exclude=_sim.used_premises + seen_premises,
                                                reserved_conclusion=None,
                                                strategy=strategy,
                                                source=source_pos,
                                                target=target_pos)
            if selected_premises:
                _found_premises = True
                seen_premises.append(selected_premises)
            else:
                # Can't find available premises.
                _sim.log.append("Can't find premises for source %s and target %s" % (source_pos, target_pos))
                _found_valid_argument = False
                break

            if _found_premises == True:
                possible_conclusions = fetch_conclusion(sentencepool=_sim.sentencepool,
                                                        exclude=And(*selected_premises).atoms(),
                                                        strategy=strategy,
                                                        source=source_pos,
                                                        target=target_pos)
                
                if len(possible_conclusions) == 0:
                    _sim.log.append("Introducing argument failed because no matching conclusion could be found for the selected premises. %d combinations of premises have been tried." % (len(seen_premises)))
                    _found_conclusion = False
                else:
                    selected_conclusion = choice(possible_conclusions)
                    _found_conclusion = True

        if _sim.debate_growth == "tree":
            possible_conclusions = fetch_conclusion(sentencepool=_sim.sentencepool,
                                                    exclude=set(),
                                                    strategy=strategy,
                                                    source=source_pos,
                                                    target=target_pos)
            if len(possible_conclusions) == 0:
                    _sim.log.append("Can't find conclusion for source %s and target %s" % (source_pos, target_pos))
                    _found_valid_argument = False
                    break
            else:
                atomic_levels = proposition_levels_from_debate(_sim[-1], key_statements=_sim.key_statements)
                levels = atomic_levels | {Not(i): atomic_levels[i] for i in atomic_levels}
                c = {i: levels[i] for i in levels if i in possible_conclusions}
                w = [0.75**i for i in c.values()]
                if w:
                    selected_conclusion = choices(list(c.keys()), weights=w)[0]
                    _found_conclusion = True
                else: 
                    _sim.log.append("Can't find conclusion that fits proposition hierarchy for source %s and target %s" % (source_pos, target_pos))
                    _found_valid_argument = False
                    break

            if _found_conclusion:
                selected_premises = select_premises(sentencepool=_sim.premise_candidates(),
                                                    length=_sim.argumentlength,
                                                    exclude=_sim.used_premises + seen_premises,
                                                    reserved_conclusion=selected_conclusion,
                                                    strategy=strategy,
                                                    source=source_pos,
                                                    target=target_pos)
                if selected_premises:
                    _found_premises = True
                    seen_premises.append(selected_premises)
                else:
                    # Can't find available premises.
                    _sim.log.append("Can't find premises for source %s and target %s" % (source_pos, target_pos))
                    _found_valid_argument = False
                    break
        
        if _found_premises and _found_conclusion:
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

        if type(_sim[-1]) == EmptyDebate:
            # Are we just beginning the debate?
            _sim.append(Debate(Argument(And(*selected_premises), selected_conclusion)))
        else:
            # If the previous debate stage was not empty, it's either a single Argument...
            if type(_sim[-1]) == Argument:
                # If a Debate conists of just one Argument, the debate's type
                # is changed to Argument b/c of inheritance from sympy cls.
                _sim.append(Debate( _sim[-1], Argument(And(*selected_premises), selected_conclusion)))
            # Or a Debate consisting of 1 or more Arguments
            else:
                # Assuming type is Debate or And
                _sim.append(Debate( *_sim[-1].args, Argument(And(*selected_premises), selected_conclusion)))

        # Store the argument in the optimiser:
        _sim.assertions.append(z3_assertion_from_argument(premises=selected_premises, 
                                                          conclusion=selected_conclusion))

        return True
        # return Argument(And(*selected_premises), selected_conclusion)
    else:
        _sim.log.append("Introduction with strategy '%s' failed. No valid combinations left in the premise pool." % (strategy["name"]) )
        return False

def response(*, 
             simulation, 
             method,
             debate=None,
             models=None,
             positions=None,  
             sentences=None):
    """
    Updating Positions in a debate.
    """

    # Defaults
    if debate == None:
        debate = simulation[-1]
    
    if positions == None:
        positions = simulation.positions[-1]

    if sentences == None:
        sentences = simulation.sentencepool

    if method == "random":
        updated_positions = []
        for p in positions:
            if satisfiability(And(dict_to_prop(p), debate)):
                updated_positions.append(p)
            else:
                u = deepcopy(p)
                u |= choice(satisfiability(And(*sentences, debate), all_models=True))
                updated_positions.append(u)
        simulation.positions.append(updated_positions)

    if method == "closest_coherent_complete_search":
        updated_positions = []
        models = list(satisfiability(debate, all_models="True"))
        examinees = [{k: i[k] for k in i if k in debate.atoms()} for i in positions]
        distances = np.array([[hamming_distance(i, j) for i in models] for j in examinees])

        for i in range(distances.shape[0]):
            if np.min(distances[i]) == 0:
                updated_positions.append(positions[i])
                simulation.log.append(
                    f"Position with index {i} did not need an update.")
            else:
                u = deepcopy(positions[i])
                update_index = choice(np.where(distances[i] == distances[i].min())[0].tolist())
                u |= models[update_index]
                updated_positions.append(u)
                simulation.log.append(
                    f"Position with index {i} was updated with strategy closest_coherent.")

        simulation.positions.append(updated_positions)

    if method == "closest_coherent":
        updated_positions = []
        if models is None:
            list_of_models = list(satisfiability(debate, all_models=True))
        else:
            list_of_models = models
        for (i, p) in enumerate(positions):
            if dpll_satisfiable(And(dict_to_prop(p), debate)):
                updated_positions.append(p)
                simulation.log.append(
                    f"Position with index {i} did not need an update.")
            else:
                u = deepcopy(p)
                u |= choice(next_neighbours(p, debate=debate, models=list_of_models))
                updated_positions.append(u)
                simulation.log.append(
                    f"Position with index {i} was updated with strategy closest_coherent.")
        simulation.positions.append(updated_positions)

    if method == "closest_closed_partial_coherent":
        """
        Find a close, closed, coherent, partial neighbour for the positions.
        """
        updated_positions = []

        for (idx, position) in enumerate(positions):
            # First, let's see whether the position has any chance wrt the updated debate:
            if dpll_satisfiable(And(dict_to_prop(position), debate)) and \
               closedness(position, debate=debate):
                    new_position = Position(debate,
                                            position,
                                            introduction_strategy=position.introduction_strategy,
                                            update_strategy=position.update_strategy)
                    simulation.log.append(
                        f"Position with index {idx} is still coherent and closed given the new debate.")
                
            else:
                simulation.log.append(
                    f"Position with index {idx} needs an update.")
                
                # Collect constraints for the current position. Empty positions pick a random 
                # singular position for bootstrapping (otherwise they'd stay empty).
                if len(position) > 0:                
                    constraints = z3_soft_constraints_from_position(position)
                else:
                    constraints = [choice([z3.Bool(str(i)) for i in debate.atoms()] \
                                         + [z3.Not(z3.Bool(str(i))) for i in debate.atoms()])]
                # Build the assertions iteratively. This is equivalent to adding 
                # soft constraints via z3.Optimize.add_soft().
                assertions = z3.If(constraints[0], 1, 0)
                for c in constraints[1:]:
                    assertions += z3.If(c, 1, 0)

                # MaxSAT iteration over k, the number of fulfilled constraints.
                k = len(constraints)
                saved_candidates = []
                while k >= 0:
                    o = z3.Optimize()
                    o.set(priority="pareto")
                    for a in simulation.assertions:
                        o.add(a)
                    o.add(assertions == k)
                    o.maximize(assertions)
                    
                    # Loop over all the solutions to the MaxSAT problem. Note that 
                    # closedness(model,return_alternative=True)[1] stores the closed version of a model.
                    candidates = []
                    base_models = [{symbols(str(i)): eval(str(m[i])) for i in m if symbols(str(i)) in position} \
                                    for m in z3_all_models(o, [z3.Bool(str(i)) for i in debate.atoms()])]
                    unique_base_models = list(unique_everseen(base_models, key=lambda item: frozenset(item.items())))

                    for m in unique_base_models:
                        candidates.append(closedness(m, debate=debate, return_alternative=True)[1])
                        differences = [k for k in m if m[k] != position[k]]
                        diff_samples = list(powerset(differences)); shuffle(diff_samples)

                        for d in diff_samples[:min(len(diff_samples), simulation.partial_neighbour_search_radius)]:
                            c = {l: position[l] for l in position if l not in differences} \
                                 | {l: m[l] for l in m if l in d}
                            
                            candidates.append(closedness(c, debate=debate, return_alternative=True)[1])

                    # Now calculate the ED() for the position to all candidates...
                    curr_candidates = candidates + saved_candidates
                    a = np.array([edit_distance(i, position) for i in curr_candidates])
                    
                    # ... and pick the min of distances, if the distance, but ...
                    if a.size > 0:
                        new_position = Position(debate,
                                            curr_candidates[choice(np.argwhere(a == np.amin(a)).flatten().tolist())],
                                            introduction_strategy=position.introduction_strategy,
                                            update_strategy=position.update_strategy)
                        
                        # ... if it is better then what would be expected at the next iteration.
                        if np.amin(a) > len(constraints)-k+1 and k > 0:
                            saved_candidates.append(new_position)
                        else:
                            break

                    # Could not determine an optimal candidate while demanding k constraints. 
                    # Decrease k and try again.
                    k -= 1
                else:
                    # This is here purely for diagnostic purposes.
                    raise Exception(f"Could not find a neighbour for position {position}.")

                simulation.log.append(
                    str(f"Position with index {idx} updated to a new position, ")
                    + str(f"edit distance {edit_distance(position, new_position)}."))
            # Found replacement for one position, continue loop with next position from
            # previous debabte stage.
            updated_positions.append(new_position)
        # Found candidates for all positions in pop. of cur. deb. stage.
        simulation.positions.append(updated_positions)