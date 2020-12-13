"""
taupy is a Python 3 library for the theory of dialectical structures.
"""

from decimal import Decimal
from fractions import Fraction
from math import log2

from .basic import Argument, Debate
from .basic import (Position, position_compatibility)
from .basic import (satisfiability_count, satisfiability, dict_to_prop, 
                    free_premises)

from .analysis import (doj, hamming_distance, normalised_hamming_distance, bna, next_neighbours, 
                       edit_distance, normalised_edit_distance, difference_matrix, spread)

from .simulation import Simulation
from .simulation import (introduce, response)

#from .graphs import graph_from_sccp, plot_map

__all__ = [
            # .basics
            'Argument', 'Debate', 'Position', 'position_compatibility',
            # .analysis tools
            'doj', 'hamming_distance', 'normalised_hamming_distance', 
            'bna', 'next_neighbours', 'edit_distance', 'normalised_edit_distance',
            'difference_matrix', 'spread',
            # .simulation
            'Simulation',
            # Common utilities
            'satisfiability_count', 'satisfiability', 'dict_to_prop',
            'free_premises',
            # Update mechanisms
            'introduce', 'response',
            # Applications of graph theory
            #'graph_from_sccp', 'plot_map'
          ]
