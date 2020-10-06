"""
taupy is a Python 3 library for the theory of dialectical structures.
"""

from decimal import Decimal
from fractions import Fraction
from math import log2

from .basic import Argument, Debate
from .basic import Position
from .basic import satisfiability_count, satisfiability, dict_to_prop

from .analysis import doj, hd, bna, next_neighbours

from .simulation import Simulation
from .simulation import introduce, introduce_random, response_random

from .graphs import plot_sccp, plot_map

__all__ = [
            # .basics
            'Argument', 'Debate', 'Position',
            # .analysis tools
            'doj', 'hd', 'bna', 'next_neighbours',
            # .simulation
            'Simulation',
            # Common utilities
            'satisfiability_count', 'satisfiability', 'dict_to_prop',
            # Update mechanisms
            'introduce', 'introduce_random', 'response_random',
            # Applications of graph theory
            'plot_sccp', 'plot_map'
          ]
