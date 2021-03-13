"""
Basic tools in simulations
"""
from sympy import symbols, Not
from itertools import combinations, chain
from random import choice, sample
from concurrent.futures import ProcessPoolExecutor, as_completed

from taupy.basic.utilities import satisfiability, satisfiability_count
from taupy import Debate, EmptyDebate
from .update import introduce, response
import taupy.simulation.strategies as strategies

class Simulation(list):
    
    def __init__(self,
                 directed=True, 
                 sentencepool="p:10",
                 sentences_sources=[],
                 sentences_sinks=[],
                 parent_debate=None,
                 argumentlength=2,
                 positions=[],
                 default_introduction_strategy = strategies.random, 
                 default_update_strategy = "closest_coherent"):
        
        if sentencepool == "inherit": # import from parent debate
            self.sentencepool = [i for i in parent_debate.atoms()]
        else:
            self.sentencepool = [i for i in symbols(sentencepool)]

        self.sources = [i for i in symbols(sentences_sources)] + [Not(i) for i in symbols(sentences_sources)]
        self.sinks = [i for i in symbols(sentences_sinks)] + [Not(i) for i in symbols(sentences_sinks)]
            
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
        # Initialise the Simulation with an empty debate. This is 
        # necessary so that the initial positions can attach to some debate.
        self.append(EmptyDebate()) if parent_debate == None else self.append(parent_debate)
        
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
        _premisepool = set(self.sentencepool + [Not(i) for i in self.sentencepool]) - set(self.sinks)
        
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
        Generate initial Positions. Optionally, the Positions may start off with
        explicit truth-value attributions. Positions are filled up with random
        values for truth-value attributions they do not yet have, such that they
        begin as complete positions.
        """
        self.positions = []

        for p in positions:
            for s in self.sentencepool:
                if s not in p:
                    p[s] = choice([True, False])

        self.positions.append(positions)
                
    def run(self, max_density=0.8, max_steps=1000, min_sccp=1, quiet=True):
        """
        Run a Simulation using ``introduction_method`` and ``update_mechanism`` 
        until either ``max_density`` is reached, the SCCP has an extension of 
        ``min_sccp`` or ``max_steps`` have been taken.
        
        If ``quiet=False``, the last log entry which contains a summary of 
        the simulation is not output. This is useful in batch processing of
        Simulations (see ``experiment()``).
        """

        i = 0

        while True:
            if self.directed and len(self.positions[-1]) >= 2:
                # The user asked for a directed simulation and has supplied
                # enough Positions.
                pick_positions = sample(self.positions[-1], k=2)
                
                # Support for positions with multiple introduction strategies. 
                # First, try to pick a random element from the list of introduction
                # strategies of a position. If that fails, assume that the strategy
                # preference of a position is not given as a list, but as a single
                # item.
                try:
                    pick_strategy = choice(pick_positions[0].introduction_strategy)
                except KeyError:
                    pick_strategy = pick_positions[0].introduction_strategy
                
                argument_introduced = introduce(self, 
                                                source=pick_positions[0],
                                                target=pick_positions[1],
                                                strategy=pick_strategy)
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
        
        if quiet:
            return self.log[-1]
        else:
            return self

def experiment(n, executor={}, simulations={}, runs={}):
    """
    Generate and execute `n` number of Simulations and output their results. 
    The Simulations can be controlled via a dictionary passed to ``simulations``.
    The ``Simulation.run()``s can be controlled with a dictionary passed to 
    ``runs``.

    Settings to the ``ProcessPoolExecutor`` should be forwarded in a dictionary
    to ``executor``.
    """
    simulations = [Simulation(**simulations) for _ in range(n)]

    with ProcessPoolExecutor(**executor) as executor:
        results = [executor.submit(i.run, quiet=False, **runs) for i in simulations]

        for count, future in enumerate(as_completed(results), start=1):
            print(f"Simulation {count}/{n} completed.")
    
    return [i.result() for i in results]
