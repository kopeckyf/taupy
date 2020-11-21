"""
Basic tools in simulations
"""

from sympy import symbols, Not
from itertools import combinations, chain
from random import choice, sample

from taupy.basic.utilities import satisfiability, satisfiability_count
from .update import (introduce, response)

class Simulation(list):
    
    def __init__(self,
                 directed=True, 
                 sentencepool="p:10", 
                 argumentlength=2, 
                 positions=[],
                 default_introduction_strategy = "random", 
                 default_update_strategy = "closest_coherent"):
        
        if sentencepool == "auto": # import from input debate
            self.sentencepool = [i for i in self.atoms()]
        else:
            self.sentencepool = [i for i in symbols(sentencepool)]
            
        self.init_premisepool(argumentlength)
        # It's a good idea to store the argument length so that other functions
        # can access that information.
        self.argumentlength = argumentlength
        self.init_positions(positions)

        self.directed = directed
        self.default_introduction_strategy = default_introduction_strategy
        self.default_update_strategy = default_update_strategy
        self.log = []        
        list.__init__(self)
        
    def init_premisepool(self, r):
        """
        A generator to obtain all premise combinations available for the 
        introduction of a new argument.
        
        In _premisepool, the closure under negation of the Simulation's
        sentencepool is generated.
        
        This pool is then filtered for configurations that are already used
        in the latest Debate stage (self[-1]), and for those combinations that
        have ~x & x in their list. The last step in particular is currently
        in need of optimisation.
        """
        _premisepool = self.sentencepool + [Not(i) for i in self.sentencepool]
        
        try: # Assume variable length of subsequence. Following an idea by Dan H.
            _iterator = chain(*map(lambda i: combinations(_premisepool, i), r))
        except TypeError: # the input r is not an iterable. Now assume integer.
            _iterator = combinations (_premisepool, r)
         
        self.premisepool = []
        for i in _iterator:
            for x in i:
                if Not(x) in i: break
            else: 
                self.premisepool.append(i)
                
    def init_positions(self, positions):
        """
        Generate initial Positions. Optionally, the Positions may start off with explicit
        truth-value attributions. This function complementises the Positions such that they
        begin as complete positions.
        """
        self.positions = []

        for p in positions:
            for s in self.sentencepool:
                if s not in p:
                    p[s] = choice([True, False])

        self.positions.append(positions)
                
    def run(self, max_density=1, max_steps=1000, min_sccp=1):
        """
        Run a Simulation using introduction_method and update_mechanism until
        either max_density is reached or max_steps have been taken.
        """

        i = 0
        # self.log.append("Directed Simulation initiated.") if self.directed else 
        # self.log.append("Undirected Simulation initiated.")

        while True:
            if self.directed and len(self.positions[-1]) >= 2:
                # The user asked for a directed simulation and has supplied
                # enough Positions.
                pick_positions = sample(self.positions[-1], k=2)
                argument_introduced = introduce(self, 
                                                source=pick_positions[0],
                                                target=pick_positions[1],
                                                strategy=pick_positions[0].introduction_strategy)
                if argument_introduced:
                    # Check if introduction was succesful before attempting response.
                    response(self, method=self.default_update_strategy)
            else:
                argument_introduced = introduce(self, strategy=self.default_introduction_strategy)
                if argument_introduced:
                    response(self, method=self.default_update_strategy)
            
            if not argument_introduced:
                # Break out of the Simulation if no argument could be inserted.
                # In this case, the log will tell more about what went wrong.
                break

            i += 1
            if self[-1].density() >= max_density or i >= max_steps or satisfiability_count(self[-1]) <= min_sccp:
                break
        self.log.append("Simulation ended. %d steps were taken. Density at end: %f. Extension of SCCP: %d." % (i, self[-1].density(),  satisfiability_count(self[-1])))
        print("Simulation ended. %d steps were taken. Density at end: %f. Extension of SCCP: %d." % (i, self[-1].density(),  satisfiability_count(self[-1])))