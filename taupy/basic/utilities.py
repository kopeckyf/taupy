try: # Assume that CUDD is installed on the system and bindings present.
    from dd.cudd import BDD
except ModuleNotFoundError:
    from dd.autoref import BDD
    print("taupy Info: Module dd.cudd not found, reverting to dd.autoref")
from sympy.logic import to_cnf, And, Implies, Not
from sympy import symbols
import numpy as np
from random import sample, choice
from itertools import chain, combinations
from more_itertools import random_combination
import math

def dict_to_prop(dictionary):
    """
    Helper function that converts a dictionary to a propositional formula,
    acknowledging dictionary's truth-value attributions.
    """
    l = []
    for (k, v) in dictionary.items():
        if v: l.append(k)
        if not v: l.append(Not(k))
    return And(*l)

def dict_to_binary(dictionary):
    """
    A helper function that converts the dictionary representation of a position
    to its presentation in a binary string.
    """
    l = []
    for k in sorted(dictionary):
        if dictionary[k]: l.append(1)
        if not dictionary[k]: l.append(0)
    return l

def free_premises(debate):
    """
    Returns a list of premises that are "free" in the sense of [1: Def. 3].
    -----
    Referenes:
    [1] Betz, Gregor. 2009. Evaluating dialectical structures. In: Journal
        of philosophical logic 38: 283--312. DOI: 10/cxrbhh
    """
    premises = set()
    for i in debate.args:
        for j in [*i.args[0].atoms()]:
            premises.add(j)
    conclusions = {i.args[1] for i in debate.args}

    return {i for i in premises if i not in conclusions and
            Not(i) not in conclusions}

def iter_to_string(l, sep=""):
    """
    Helper function that converts a dictionary position to a bit string.
    """
    return sep.join(str(i) for i in l)

def iter_to_list_of_strings(l):
    return [str(i) for i in l]

def neighbours_of_list(l):
    """
    Find the neighbours of a position in list format. A neighbour is a position
    that has HD = 1 to the position in question.
    """
    complements = [1,0] # complements[0] == 1 and complements[1] == 0
    for i in range(len(l)):
        yield (l[:i] + [complements[l[i]]] + l[i+1:])

def satisfiability_count(formula):
    """
    Count the models that satisfy a Boolean formula, using Binary decision diagrams.
    """
    variables = iter_to_list_of_strings(formula.atoms())
    diagram = BDD()
    diagram.declare(*variables)
    expression = diagram.add_expr(str(to_cnf(formula)))
    return int(diagram.count(expression, nvars=len(formula.atoms())))

def satisfiability(formula, all_models = False):
    """
    Return a generator of models for the given Boolean formula, using BDDs
    """
    variables = iter_to_list_of_strings(formula.atoms())
    diagram = BDD()
    diagram.declare(*variables)

    if all_models:
        expression = diagram.add_expr(str(to_cnf(formula)))
        return [{symbols(k): v for (k, v) in m.items()} for m in \
            diagram.pick_iter(expression, care_vars={str(i) for i in \
                formula.atoms()})]
    else:
        try:
            expression = diagram.add_expr(str(to_cnf(formula)))
            next(diagram.pick_iter(expression))
            return True
        except StopIteration:
            return False

def satisfiable_extensions(debate, position):
    """
    Return all extensions of a (partial) position relative to a debate. If the position is
    complete and satisfiable, it is returned as a satisfiable extension of itself. If it is
    a partial position and satisfiable, complete positions that extend it are returned.
    """
    # The union of propositions in the position and debate is used here in case the position
    # has a stance toward a proposition that is not yet part of an argument.
    variables = list({str(i) for i in debate.atoms()} | {str(i) for i in position.keys()})
    diagram = BDD()
    diagram.declare(*variables)

    expression = diagram.add_expr(str(to_cnf(debate)))
    for m in diagram.pick_iter(expression, care_vars={str(i) for i in variables}):
        yield {symbols(k): v for (k, v) in m.items()}

def graph_from_positions(positions, return_attributions=False):
    """
    Returns a dictionary of lists (position: [neighbour1, neighbour2, ...])
    that resembles the space of the positions.

    If return_attributions is set to True, this function returns a tuple. The
    first object then is the graph representation in a dict of lists format, the
    second object is a mapping from the string representation of a position
    to its dictionary format. This is useful because non-hashable objects like
    dictionaries can not be used as identifiers of nodes in graphs.
    """
    d = {}
    props = sorted(positions[0].keys(), key=lambda x: x.sort_key())
    bits = [list (1 if p[i] else 0 for i in props) for p in positions]
    for b in bits:
        neighbourlist = [iter_to_string(x) for x in neighbours_of_list(b) if x in bits]
        d[iter_to_string(b)] = neighbourlist
    if return_attributions:
        return d, dict(zip(list(iter_to_string(b) for b in bits), positions))
    else:
        return d

def rand_index(partition1, partition2):
    """
    Calculate Rand's index, a measure of similarity for two data clusterings.
    Not yet implemented.
    """
    pass

def ari(partition1, partition2):
    """
    Calculate the Adjusted Rand Index.
    """
    # First, let's look at the number of elements
    if sum(len(l) for l in partition1) != sum(len(l) for l in partition2):
        raise ValueError("The two partitions have a different number of elements.")
    else:
        num_of_elements = sum(len(l) for l in partition1)

    contingency = contingency_matrix(partition1, partition2)
    sums_of_columns = contingency.sum(axis=0)
    sums_of_rows = contingency.sum(axis=1)

    columns = sum([n * (n-1)/2 for n in sums_of_columns])
    rows = sum([n * (n-1)/2 for n in sums_of_rows])
    elements = sum([n * (n-1)/2 for n in np.nditer(contingency)])
    expected_value = columns * rows / (num_of_elements * (num_of_elements-1)/2)

    return (elements - expected_value) / ((1/2 * (rows + columns)) - expected_value)

def contingency_matrix(partition1, partition2):
    """
    A contingency matrix, a necessary indegredient for Rand's index and the ARI.
    """
    return np.array(
        [[len(set(j) & set(k)) for j in partition1] for k in partition2]
    )

def pick_random_positions_from_debate(n, debate):
    """
    A helper function to pull `n` random positions from a debate's SCCP. Returns
    :py:obj:`False` if the debate's SCCP is smaller than `n`.
    """
    if satisfiability_count(debate) >= n:
        # Using satisfiability_count() here can spare us the construction of
        # a SCCP, which is more complex than just obtaining the SCCP's number.
        return sample(population=satisfiability(debate, all_models=True), k=n)
    else:
        return False

def subsequences_with_length(iterable, length):
    """
    A helper function to return all subsequences with a length of `length`.
    This is useful when used incrementally: rather than generating the complete
    power set, work your way up and work with what you get at every `length`.
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(length+1))

def fetch_conclusion(*, sentencepool, exclude, strategy, source, target):
    """
    Finds a proposition from the `sentencepool` that is not already in `exclude`
    but which fits the introduction `strategy` and the belief systems of 
    `source` and `target`.
    """
    # Get the conclusion candidates from the sentence pool
    possible_conclusions = list(set(sentencepool) - set(exclude))
    possible_conclusions += list(Not(i) for i in possible_conclusions)

    # Directed strategies act as filters on possible conclusions. The list of possible values is not exhausted b/c it is not required by the currently known strategies.
    if strategy["source_accepts_conclusion"] == "Yes":
        possible_conclusions = list(set(possible_conclusions) & set(dict_to_prop(source).args))

    if strategy["source_accepts_conclusion"] == "Toleration":
        possible_conclusions = list(set(possible_conclusions) - {Not(i) for i in dict_to_prop(source).args})

    if strategy["target_accepts_conclusion"] == "No":
        possible_conclusions = list(set(possible_conclusions) - set(dict_to_prop(target).args))
    
    return possible_conclusions

def fetch_premises(pool, length, exclude=[]):
    """
    Fetch a combination of premises with length `n` from the input pool of
    sentences. This function will not return a combination of premises that
    is mentioned in `exclude`.

    This way of iteratively drawing a random sample has no natural breakpoint
    (i.e., there is no iterator that is empty at some point). Thus we estimate
    that there are at most (k over n) tries, where k is the length of the
    pool and `n` the desired length. The main weakness of this approach
    is that it can theoretically happen that the only available combination
    is not reached before the maximum amount of tries is done.
    """

    try:
        n = choice(length)
    except TypeError:
        n = length

    j = 0
    k = math.comb(len(pool), n)

    while True:
        if j < k:
            i = random_combination(pool, n)
            if i not in exclude:
                for x in i:
                    if Not(x) in i: break
                else:
                    return i
            j += 1
        else:
            return False

def select_premises(*, sentencepool, length, exclude, 
                    reserved_conclusion=None, strategy, source, target):
    """
    Select fetched premises based on whether they fit an argument strategy.
    """
    if reserved_conclusion == None:
        conclusion_set = set()
    else:
        conclusion_set = {reserved_conclusion, Not(reserved_conclusion)}        

    if strategy["pick_premises_from"] == None:
        pool = sentencepool - conclusion_set
    else:
        if strategy["pick_premises_from"] == "source":
            pool = set(dict_to_prop(source).args) - conclusion_set
        if strategy["pick_premises_from"] == "target":
            pool = set(dict_to_prop(target).args) - conclusion_set

    return fetch_premises(pool, length=length, exclude=exclude)

def proposition_levels_from_debate(debate, key_statements=[]):
    """
    Return a dictionary of levels, following an idea by Vera Chekan.

    Next level: Is it possible to determine key statements in a debate automatically?
    """
    if not key_statements:
        # Check if a list of key statements is provided.
        raise ValueError("Key statements are required to calculate levels.")
    
    # Key statements receive level 0
    levels = {k: 0 for k in key_statements}
    if len(debate.args) > 2:
        # Check if the debate has any Arguments.
        conclusions = [next(iter(a.args[1].atoms())) for a in debate.args]
    else:
        # This case holds if the Debate does not contain any Arguments, e.g. 
        # if it is an EmptyDebate.
        conclusions = []
    i = 0

    while True:
        if any(levels[c] == i for c in conclusions if c in levels):
            for argument in debate.args:
                c = next(iter(argument.args[1].atoms()))
                if c in levels and levels[c] == i:
                    for p in argument.args[0].atoms():
                        if p not in levels:
                            levels[p] = i+1
            i += 1
        else:
            break

    if len(levels) != len(debate.atoms()) and __name__ == "__main__":
        print("taupy Warning: Not all propositions received a level. Maybe the input debate \
               did not have a connected argument map?")

    return levels
