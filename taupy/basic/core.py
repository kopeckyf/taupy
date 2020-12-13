from decimal import Decimal
from itertools import combinations
from math import log2
from sympy.logic import (And, Implies, Not)
from .utilities import (iter_to_string, neighbours_of_list, 
                        satisfiability_count, satisfiability)
from taupy.analysis.agreement import edit_distance


class Base():
    
    def sccp(self):
        """
        Returns a dictionary of lists (position: [neighbour1, neighbour2, ...])
        that resembles the space of coherent and complete positions. This 
        structure serves as the basis for graph analysis and graph drawing.
        
        Iteration is done over the possible neighbours of a position rather than
        with all other positions, b/c the searches' complexity will be lower.
        """
        _d = {}
        _pos = [p for p in satisfiability(self, all_models=True)]
        _props = sorted(_pos[0].keys(), key=lambda x: x.sort_key())
        _bits = [list (1 if _p[_i] else 0 for _i in _props) for _p in _pos]
        for _b in _bits:
            _neighbourlist = [iter_to_string(x) for x in neighbours_of_list(_b) if x in _bits]
            _d[iter_to_string(_b)] = _neighbourlist
        return _d
    
    def weighted_sccp(self, distance_measure=edit_distance):
        """
        Return 
        """
        _d = {}
        _sat = satisfiability(self, all_models=True)
        _combs = combinations(satisfiability(self, all_models=True), r=2)
        _props = sorted(_sat[0].keys(), key=lambda x: x.sort_key())
        for c in _combs:
            _bits = [list(1 if j[i] else 0 for i in _props) for j in c]
            _d.setdefault(iter_to_string(_bits[0]),{}).update({iter_to_string(_bits[1]): {"weight": 1 / distance_measure(c[0], c[1])}})
        
        return _d
    
    def map(self, method = "plain"):
        """
        Returns the plot of the argument map.
        """
        
        _conclusions = [(i, c.args[1]) for i, c in enumerate(self.args)]
        _premises = [(i, p.args[0].args) for i, p in enumerate(self.args)]
        
        if method == "plain":
            _result = {}
            for (i, _conc) in _conclusions:
                _innerdict = {}
                for (j, _prems) in _premises:
                    if _conc in _prems:
                        _innerdict [j] = {"edge_color": "support"}
                    if Not(_conc) in _prems:
                        _innerdict [j] = {"edge_color": "attack"}
                _result [i] = _innerdict
            return _result
        
        if method == "networkx":
            pass
        
        if method == "graphtool":
            pass                
    
    def density(self):
        _sigma = satisfiability_count ( self )
        return Decimal ((len(self.atoms()) - log2(_sigma)) / len(self.atoms()))
    
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
    Must protect against Inputs like Argument((a,b),c)!
    """
    pass
    
class Debate(And, Base):
    """
    Debates
    """
    def __init__(self, *args): # Check *args
        And.__init__(self)
        self.actual_positions = []
