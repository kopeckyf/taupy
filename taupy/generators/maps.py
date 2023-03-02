"""
Generators for argument maps.
"""

from taupy.basic.core import EmptyDebate, Debate, Argument
from taupy.basic.utilities import proposition_levels_from_debate, premise_usage_count
from sympy import Not, And, symbols
from sympy import satisfiable as dpll_satisfiability
from random import choices
import numpy as np

def generate_hierarchical_argument_map(N = 20, 
                                       k = 3,
                                       max_num_args = float("inf"),
                                       max_density = 1.0,
                                       distribution = {2: 0.19, 3: 0.23, 
                                                       4: 0.32, 5: 0.26},
                                       base_conclusion = 0.75,
                                       base_premises = 0.75):

    """
    Generate a hierarchical synthetic argument map, following the algorithm from 
    Betz, Chekan & Mchedlidze ([Betz2021]_).
    """   
    
    d = EmptyDebate()
    # Construct N propositional variables
    sentencepool = list(symbols(f"p:{N}"))
    # The first k elements are key statements.
    key_statements = sentencepool[:k]

    while len(d.args) < max_num_args and d.density() < max_density:
        atomic_levels = proposition_levels_from_debate(
            d, key_statements=key_statements
            )

        levels = atomic_levels | {Not(i): atomic_levels[i] for i in atomic_levels}
        w = [base_conclusion**i for i in levels.values()]

        selected_conclusion = choices(list(levels.keys()), weights=w)[0]

        premise_usage = premise_usage_count(d, premises=sentencepool)
        del premise_usage[selected_conclusion]
        del premise_usage[Not(selected_conclusion)]
        v = [base_premises**i for i in premise_usage.values()]
        # Normalised weights for premises
        vis = [i/sum(v) for i in v]
        # Number of premises for current argument
        n = choices(list(distribution.keys()), weights=list(distribution.values()))[0]

        selected_premises = np.random.choice(list(premise_usage.keys()), size=n, p=vis, replace=False)
        
        if dpll_satisfiability(And(*selected_premises)):
            a = Argument(And(*selected_premises), selected_conclusion)
            if dpll_satisfiability(And(d, a)):
                if type(d) == Argument:
                    d = Debate(d, a)
                else:
                    d = Debate(*d.args, a)

    return d