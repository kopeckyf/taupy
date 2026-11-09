from taupy.basic.core import Argument, Debate
from taupy.basic.utilities import z3_solver_status
from taupy.analysis.agreement import edit_distance
from taupy.analysis.doj import doj
from sympy import Not, Or, Implies, parse_expr
import z3
import random
import pandas as pd

def determine_defeaters(arguments):
    """
    Create a mapping of arguments to their defeaters, in the typical sense of
    "defeat" in the theory of dialectical structures.
    
    Returns a mapping {'a1': [List of 'defeaters' of a1], ...}
    """
    defeaters = dict()
    if type(arguments) is not Argument:
        for a in arguments:
            defeaters[str(a)] = []
            for b in arguments:
                if Not(b.args[1]) in a.args[0].args:
                    defeaters[str(a)] += [str(b)]
    return defeaters

def all_validity_functions(argumentmap):
    """
    Determine all dialectical validity functions for an argument map, in the 
    sense of Betz (2009, Def. 2).
    """
    solver = z3.Solver()
    relations = determine_defeaters(argumentmap)
    arguments = relations.keys()
    z3_symbols = {a: z3.Bool(a) for a in arguments}

    for a in arguments:
        defeaters = relations[a]
        if defeaters:
            # An argument is dialectically valid iff all defeaters are dialectically invalid
            solver.add(z3_symbols[a] == z3.And([z3.Not(z3_symbols[d]) for d in defeaters]))
        else:
            # Arguemnts without defeaters are valid
            solver.add(z3_symbols[a] == z3.BoolVal(True))

    validity_functions = []
    # The usual blocking approach to the ALLSAT problem:
    while solver.check() == z3.sat:
        model = solver.model()
        # Found one solution to assign a validity function. Add it...
        solution = {a: bool(model[z3_symbols[a]]) for a in arguments}
        validity_functions.append(solution)

        # ... block the current solution, and check again:
        solver.add(z3.Or([
            z3_symbols[a] != model[z3_symbols[a]]
            for a in arguments
        ]))

    return validity_functions

def is_validity_function(stance, argumentmap):
    """
    Check whether the `stance` is a validity function for `argumentmap`, in the
    sense of Betz (2009, Def. 2).
    """
    solver = z3.Solver()
    relations = determine_defeaters(argumentmap)
    arguments = relations.keys()
    z3_symbols = {a: z3.Bool(a) for a in arguments}

    for a in arguments:
        defeaters = relations[a]
        if defeaters:
            # An argument is dialectically valid iff all defeaters are dialectically invalid
            solver.add(z3_symbols[a] == z3.And([z3.Not(z3_symbols[d]) for d in defeaters]))
        else:
            # Arguemnts without defeaters are valid
            solver.add(z3_symbols[a] == z3.BoolVal(True))
    
    for argument, validity in stance.items():
        # validity is either True or False
        solver.add(z3_symbols[str(argument)] == z3.BoolVal(validity))

    return z3_solver_status(solver)
    
def accepted_propositions(validity_function):
    """
    Return all accepted propositions given a dialectical validity function.
    A proponent accepts (Betz 2009, Def. 6):
     - All free premises (in valid and invalid arguments).
     - The conclusions of valid arguments.
    """
    
    # Using eval() here is not pretty, but the world is a messy place.
    valid_arguments = []
    invalid_arguments = []
    for argument, validity in validity_function.items():
        # I don't like to rely on sympy.parse_expr(), but it's the best method 
        # to transfer data between sympy and z3 until I settle on a permanent 
        # solution.
        if validity:
            valid_arguments.append(parse_expr(argument))
        else:
            invalid_arguments.append(parse_expr(argument))

    accepted_premises = set()
    accepted_conclusions = set()

    # Step 1: Add all premises and conclusions of valid arguments to the
    #         set of accepted propositions
    for a in valid_arguments:
        # add all premises from the argument
        for premise in a.args[0].args:
            accepted_premises.add(premise)
        # add the argument's conclusion
        accepted_conclusions.add(a.args[1])
    
    # Step 2: Add all free premises from invalid arguments
    for a in invalid_arguments:
        for premise in a.args[0].args:
            if (Not(premise) not in accepted_conclusions) and (premise not in accepted_conclusions):
                accepted_premises.add(premise)

    return accepted_premises | accepted_conclusions

def commitments(acceptability_function):
    """
    accepted_propositions() return the commitments of a validity function as 
    a set. This function returns equivalent information as a mapping.
    """
    accepted = accepted_propositions(acceptability_function)
    d = dict()
    for p in accepted:
        if p.is_Not:
            # Since Not(Not(p)) == p, the following will create a d[p] entry.
            d[Not(p)] = False
        else:
            d[p] = True
    return d

def equilibrium(propositions):
    """
    Determine whether a set of propositions is in equilibrium, loosely in the 
    sense of Betz (2009, Def. 5).
    """
    for p in propositions:
        if Not(p) in propositions:
            return False
    else:
        return True

def dialectical_closedness(validity_function, parent_debate, *, acceptance=None):
    """
    Loop over all arguments in the `parent_debate` that are not already in the
    `validity_function` and return the list of arguments that only have premises 
    which are accepted propositions given the `validity_function` (following
    Betz, 2009, Def. 7). 
    """
    if acceptance == None:
        accepted = accepted_propositions(validity_function)
    else:
        accepted = acceptance
    candidates = []
    for a in parent_debate:
        if str(a) not in validity_function:
            if set(a.args[0].args).issubset(accepted):
                candidates.append(a)
    return candidates

def responsiveness(validity_function, statement, *, thresholds=[.49,.51]):
    """
    Check whether the `validity_function` responds to its evidence regarding
    `statement`. This means that the function accepts `statement` if, from its
    standpoint, `statement` is justified. Allows fuzzy `thresholds`.
    """
    dojtheta = float(doj(
                {statement: True},
                Debate(
                    Or(statement, Not(statement)),
                    *[parse_expr(a, local_dict={"Argument": Implies}) 
                      for a, v in validity_function.items() if v]
                    )
                    )
                )

    accepted = accepted_propositions(validity_function)

    if dojtheta < thresholds[0] and statement in accepted:
        # From the perspective of `validity_function`, the `statement` is not
        # well justified. But `statement` is in the propositions that 
        # `validity_function` accepts. That is a violation of responsiveness.
        return False
    if dojtheta > thresholds[1] and Not(statement) in accepted:
        # From the perspective of `validity_function`, the `statement` is 
        # well justified. But the negation of `statement` accepted by 
        # `validity_function`. That is a violation of responsiveness.
        return False
    
    return True

class Stance():
    """
    A stance is one type of response to an argument map. Agents who have a 
    stance decide whether to maintain or reject an argument. This is different
    from Position()s, which agents use to form beliefs about propositions in
    light of arguments.

    Stances were introduced to the theory of dialectical structures early 
    (in Betz, 2009), but the original simulation studies (Betz, 2013) were
    only about positions. Stances are acceptability functions. This is the
    behavior that Dung (1995) thought of when he modelled how agents would 
    respond to an argument map.

    The purpose of this module is to understand the difference between stances
    (acceptability functions) and positions (belief systems).

    This Stance class is dis-analogouos to the Position class in the positions
    module as it has built-in exploration features in its step() and run() 
    methods. This will have to be harmonized when I find the time for it.
    """
    def __init__(
            self, 
            parent_debate, 
            *, 
            key_statement=None, 
            init_argument=True
            ):

        self.debate = parent_debate
        self.data = []
        self.validity_functions = [dict()]

        if key_statement == None:
            self.key_statement = self.debate.sentencepool[0]
        else:
            self.key_statement = key_statement

        if self.key_statement:
            self.objective_doj = float(
                doj({self.key_statement: True}, Debate(*self.debate.args))
                )
        else:
            self.objective_doj = "NaN"

        if init_argument:
            # Initialize the Stance with a random argument that contains 
            # `key_statement`
            random_init = random.choice(
                [argument for argument in self.debate.args if 
                 self.key_statement in argument.atoms()]
            )
            if random_init:
                # Initialize with the newly found argument
                self.validity_functions.append(
                    {str(random_init): True}
                )
                stance_current_doj = self.current_doj()
                self.data.append(
                    {
                        "step": len(self.data)+1,
                        "numargs": len(self.validity_functions[-1]),
                        "sizeargs": 
                            len(self.validity_functions[-1])/len(self.debate),
                        "dojtheta": stance_current_doj,
                        "objectivedoj": self.objective_doj,
                        "bias": stance_current_doj - self.objective_doj,
                        "accepts": self.key_statement_accepted()
                    }
                )
            else:
                raise ValueError(
                    f"No argument with key statement {self.key_statement} \
                      found in {self.debate}."
                )


    def current_arguments(self):
        return [parse_expr(k) for k in self.validity_functions[-1]]
    
    def current_doj(self):
        """
        How well is the key statement justified, given the currently accepted 
        arguments?
        """
        return float(
            doj(
                {self.key_statement: True},
                Debate(
                    Or(self.key_statement, Not(self.key_statement)),
                    *[parse_expr(a, local_dict={"Argument": Implies}) 
                      for a, v in self.validity_functions[-1].items() if v]
                )
            )
        )

    def key_statement_accepted(self):
        """
        Check whether the key statement of a stance is currently accepted by it.
        """
        return self.key_statement in accepted_propositions(self.validity_functions[-1])
    
    def step(self):
        """
        Search for new arguments in `parent_debate` and add an argument with
        minimal updating costs.
        """
        candidate_functions = []
        for argument in self.debate.args:
            if str(argument) not in self.validity_functions[-1]:
                # For the union of known arguments and new argument, 
                # determine all validity functions:
                for candidate_function in all_validity_functions(
                    [*self.current_arguments(), argument]
                ):
                    # Ensure that all candidates are closed.  
                    current_closure = dialectical_closedness(
                        candidate_function, self.debate.args
                        )
                    closure_constraints = {
                        parse_expr(a) for a in candidate_function
                        } | set(current_closure)
                    current_commitments = commitments(
                        self.validity_functions[-1]
                        )
                    # Would we still be in equilibrium if we followed the 
                    # candidate where it would leads us?
                    for closed_candidate in all_validity_functions(
                        closure_constraints
                        ):
                        if equilibrium(accepted_propositions(closed_candidate)):
                            # We found a closed and consistent candidate. If 
                            # it's responsive, add it.
                            if responsiveness(
                                closed_candidate, self.key_statement
                                ):
                                candidate_functions.append(
                                    (
                                        closed_candidate,
                                        edit_distance(
                                            current_commitments,
                                            commitments(closed_candidate)
                                            )
                                    )
                                )
                                # candidate_functions is low a list of pairs 
                                # [(i1,j1),(i2,j2),...], where i is a closed,
                                # consistent and responsive candidate. j is i's 
                                # distance to the current validity function.
                                # Maximizing persistence means picking one of
                                # the i's with minimal j.
        
        if candidate_functions:
            # find the minimum distance of any candidate
            optimum = min([j for i,j in candidate_functions])
            # select a random candidate that has minimal distance
            optimal_candidates = [i for i,j in candidate_functions 
                                  if j == optimum]
            return random.choice(optimal_candidates)
        else:
            return False
    
    def run(self):

        while True:
            # Look for a new argument.
            new_argument = self.step()
            if new_argument:
                # Found a new argument
                self.validity_functions.append(new_argument)
                stance_current_doj = self.current_doj()
                self.data.append(
                    {
                        "step": len(self.data)+1,
                        "numargs": len(self.validity_functions[-1]),
                        "sizeargs": len(self.validity_functions[-1])/len(self.debate),
                        "dojtheta": stance_current_doj,
                        "objectivedoj": self.objective_doj,
                        "bias": stance_current_doj - self.objective_doj,
                        "accepts": self.key_statement_accepted()
                    }
                )
            if not new_argument:
                # End simulation if no new arguments can be found.
                break
        
        return pd.DataFrame(self.data)