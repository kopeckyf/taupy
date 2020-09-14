"""
taupy is a Python 3 library for the theory of dialectical structures.
"""

from decimal import Decimal
from fractions import Fraction
from math import log2

from .basic import Argument, Debate
from .basic import Position
from .basic import satisfiability_count, satisfiability, dict_to_prop

from .analysis import doj, hd, bna

from .simulation import Simulation
from .simulation import introduce_random, introduce, response_random

__all__ = [
            # .basics
            'Argument', 'Debate', 'Position',
            # .analysis tools
            'doj', 'hd', 'bna',
            # .simulation
            'Simulation',
            # Common utilities
            'satisfiability_count', 'satisfiability', 'dict_to_prop',
            # Update mechanisms
            'introduce_random', 'introduce', 'response_random'
          ]