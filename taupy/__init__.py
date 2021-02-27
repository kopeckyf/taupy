"""
taupy is a Python 3 library for the theory of dialectical structures.
"""

from decimal import Decimal
from fractions import Fraction
from math import log2

from .basic import Argument, Debate
from .basic import (Position, position_compatibility)
from .basic import (satisfiability_count, satisfiability, dict_to_prop, 
                    dict_to_binary,
                    free_premises, graph_from_positions, ari)

from .analysis import (doj, hamming_distance, normalised_hamming_distance, bna, next_neighbours, 
                       edit_distance, normalised_edit_distance, difference_matrix, spread, lauka,
                       pairwise_dispersion, group_divergence, group_consensus, group_size_parity)

from .simulation import (Simulation, experiment, introduce, response)

from .graphs import graph_from_sccp, graph_from_weighted_sccp
                    # plot_map

__all__ = [
            # .basics
            'Argument', 'Debate', 'Position', 'position_compatibility',
            # .analysis tools
            'doj', 'hamming_distance', 'normalised_hamming_distance', 
            'bna', 'next_neighbours', 'edit_distance', 'normalised_edit_distance',
            'difference_matrix', 'spread', 'lauka', 'pairwise_dispersion',
            'group_divergence', 'group_consensus', 'group_size_parity',
            # .simulation
            'Simulation', 'experiment',
            # Update mechanisms
            'introduce', 'response',
            # Common utilities
            'satisfiability_count', 'satisfiability', 'dict_to_prop',
            'dict_to_binary',
            'free_premises', 'graph_from_positions', 'ari',
            # Applications of graph theory
            'graph_from_sccp', 'graph_from_weighted_sccp'
            # 'plot_map'
          ]
