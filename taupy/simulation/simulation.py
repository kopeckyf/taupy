"""
Basic tools in simulations
"""

from sympy import symbols, Not

class Simulation(list):
    def __init__(self, sentencepool="p:10"):
        self.sentencepool = [i for i in symbols(sentencepool)]
        list.__init__(self)
