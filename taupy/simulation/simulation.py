"""
Basic tools in simulations
"""

from sympy import symbols, Not
from itertools import combinations, chain
from random import choice

from taupy.basic.utilities import satisfiability
from .update import (introduce, introduce_random, 
                     closest_coherent)

class Simulation(list):
    
    def __init__(self, sentencepool="p:10", argumentlength=2, positions=[]):
        if sentencepool == "auto": # import from input debate
            self.sentencepool = [i for i in self.atoms()]
        else:
            self.sentencepool = [i for i in symbols(sentencepool)]
            
        self.init_premisepool(argumentlength)
        self.init_positions(positions)
        
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
        """"
        Generate initial Positions based on facultative information about these
        Positions.
        
        Since the names for sentences are usually not defined in the global namespace,
        it is best to manually assign values according to their ID.
        """
        self.positions = []
        _positions = []
        
        for p in positions:
            _positions.append( { s: p[s] if s in p else choice([True, False]) for s in self.sentencepool } )        
        
        self.positions.append(_positions)
        
    def run(self, max_density = 1, max_steps = 1000, 
            introduction_method = introduce_random, 
            update_mechanism = closest_coherent):
        """
        Run a Simulation using introduction_method and update_mechanism until
        either max_density is reached or max_steps have been taken.
        """
        i = 0
        while True:            
            introduce(self, introduction_method(self))
            update_mechanism(self)
            
            i += 1
            if self[-1].density() >= max_density or i >= max_steps:
                break
        print("Simulation ended. %d steps were taken." % (i))
