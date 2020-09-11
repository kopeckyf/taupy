"""
Basic tools in simulations
"""

from sympy import symbols, Not
from itertools import combinations, chain

class Simulation(list):
    
    def __init__(self, sentencepool="p:10", argumentlength=2):
        if sentencepool == "auto": # import from input debate
            self.sentencepool = [i for i in self.atoms()]
        else:
            self.sentencepool = [i for i in symbols(sentencepool)]
            
        self.init_premisepool(argumentlength)
        
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
            _iterator = chain( *map (lambda i: combinations( _premisepool, i ),
                                     r ) )
        except TypeError: # the input r is not an iterable. Now assume integer.
            _iterator = combinations ( _premisepool , r )
         
        self.premisepool = []
        for i in _iterator:
            for x in i:
                if Not(x) in i: break
            else: 
                self.premisepool.append(i)