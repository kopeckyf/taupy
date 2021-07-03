from decimal import Decimal
from itertools import combinations
from math import log2
from sympy.logic import (And, Implies, Not)
from sympy.logic.boolalg import BooleanTrue
from .utilities import (iter_to_string, neighbours_of_list, 
                        satisfiability_count, satisfiability)
from taupy.analysis.agreement import edit_distance


class Base():
    def sccp(self, return_attributions=False):
        """
        Returns a dictionary of lists (position: [neighbour1, neighbour2, ...])
        that resembles the space of coherent and complete positions. This 
        structure serves as the basis for graph analysis and graph drawing. 
        
        Iteration is done over the possible neighbours of a position rather than
        with all other positions, b/c the searches' complexity will be lower.

        If return_attributions is set to True, this function returns a tuple. The
        first object then is the graph representation in a dict of lists format, the
        second object is a mapping from the string representation of a position
        to its dictionary format. This is useful because non-hashable objects like 
        dictionaries can not be used as identifiers of nodes in graphs.
        """
        d = {}
        positions = [p for p in satisfiability(self, all_models=True)]
        propositions = sorted(positions[0].keys(), key=lambda x: x.sort_key())
        bits = [list (1 if p[i] else 0 for i in propositions) for p in positions]
        for b in bits:
            neighbourlist = [iter_to_string(x) for x in neighbours_of_list(b) if x in bits]
            d[iter_to_string(b)] = neighbourlist
        if return_attributions:
            return d, dict(zip(list(iter_to_string(b) for b in bits), positions)) 
        else:
            return d
    
    def weighted_sccp(self, distance_measure=edit_distance):
        """
        Return a weighted SCCP, useful for measures other than the Hamming
        distance.
        """
        d = {}
        sat = satisfiability(self, all_models=True)
        combs = combinations(satisfiability(self, all_models=True), r=2)
        props = sorted(sat[0].keys(), key=lambda x: x.sort_key())
        for c in combs:
            bits = [list(1 if j[i] else 0 for i in props) for j in c]
            d.setdefault(iter_to_string(bits[0]),{}).update({iter_to_string(bits[1]): {"weight": 1 / distance_measure(c[0], c[1])}})
        
        return d
    
    def argument_map(self, method="plain"):
        """
        Create an argument map of the input debate.
        
        Note
        ----
        ``taupy`` is not designed to be an argument/debate visualisation tool.
        The `argument_map()` function is intented as a very rudimentary option for quick
        visualitions. Users looking for comprehensive argument and debate 
        visualisation are advised to take a look at Argdown.
        """
        conclusions = [(i, c.args[1]) for i, c in enumerate(self.args)]
        premises = [(i, p.args[0].args) for i, p in enumerate(self.args)]
        
        if method == "plain":
            result = {}
            for (i, c) in conclusions:
                innerdict = {}
                for (j, p) in premises:
                    if c in p:
                        innerdict[j] = {"edge_color": "support"}
                    if Not(c) in p:
                        innerdict[j] = {"edge_color": "attack"}
                result[i] = innerdict
            return result
        
        if method == "networkx":
            pass
        
        if method == "graphtool":
            pass                
    
    def density(self):
        """
        Return the dialectical density of the Debate object, as defined by Betz
        (2013: 44-49).
        
        References
        ----------
        Betz, Gregor. 2013. Debate dynamics: How controversy improves our beliefs. 
        Springer. DOI: 10/d3cx
        """
        sigma = satisfiability_count(self)
        return Decimal((len(self.atoms()) - log2(sigma)) / len(self.atoms()))
    
    def list_of_premises(self):
        """
        Returns a list with tuples containing the premises used in the Debate's Arguments.
        """
        return [p.args[0].args for p in self.args]

    def list_of_positions(self, coherent=True, complete=True):
        """
        Return the list of valid positions of a taupy object. 
        
        Todo: Currently outputs coherent and complete co&co positions only
              but should be extended later to output other configurations 
              as well.
        """
        return [p for p in satisfiability(self, all_models=True)]

class Argument(Implies, Base):
    """
    TODO: Must protect against Inputs like Argument((a,b),c)!
    """
    pass
    
class Debate(And, Base):
    """
    Debates
    """
    def __init__(self, *args): # Check *args
        And.__init__(self)
        self.actual_positions = []
        
class EmptyDebate(BooleanTrue, Base):
    """
    An empty debate dummy object. Useful places include:
 
     - Simulations are started with an EmptyDebate object so that
       the inferential density equals 0 at that debate stage.
    """
    pass
