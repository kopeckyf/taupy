"""
taupy is a Python 3 library for the theory of dialectical structures.
"""

from decimal import Decimal
from fractions import Fraction
from math import log2

from .basic import Argument, Debate
from .basic import Position

from .analysis import doj, hd, bna

from .simulation import Simulation

__all__ = [
            # .basics
            'Argument', 'Debate', 'Position',
            # .analysis tools
            'doj', 'hd', 'bna',
            # .simulation
            'Simulation'
          ]