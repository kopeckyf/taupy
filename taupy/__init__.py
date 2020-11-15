"""
taupy is a Python 3 library for the theory of dialectical structures.
"""

from decimal import Decimal
from fractions import Fraction
from math import log2

from .basic import Argument, Debate
from .basic import (Position, position_compatibility, position_inverse)
from .basic import (satisfiability_count, satisfiability, dict_to_prop, 
                    free_premises)

from .analysis import (doj, hamming_distance, bna, next_neighbours, 
                       edit_distance)

from .simulation import Simulation
from .simulation import (introduce, introduce_strategical, response_random, 
                         closest_coherent)

#from .graphs import graph_from_sccp, plot_map

__all__ = [
            # .basics
            'Argument', 'Debate', 'Position', 'position_compatibility',
            'position_inverse',
            # .analysis tools
            'doj', 'hamming_distance', 'bna', 'next_neighbours', 'edit_distance',
            # .simulation
            'Simulation',
            # Common utilities
            'satisfiability_count', 'satisfiability', 'dict_to_prop',
            'free_premises',
            # Update mechanisms
            'introduce', 'introduce_strategical', 'response_random', 
            'closest_coherent',
            # Applications of graph theory
            #'graph_from_sccp', 'plot_map'
          ]
