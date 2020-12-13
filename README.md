# taupy

## Dependencies
 - Requires Python 3.9
 - [sympy](https://github.com/sympy/sympy), for its Boolean algebra
 - [dd](https://github.com/tulip-control/dd), to create BDDs to check satisfiability as well as listing models and counting their number
 - [graph_tool](https://git.skewed.de/count0/graph-tool), for graph analysis and plotting
 
## Examples of usage
In place of a in-depth documentation, some examples for taupy's current functions and classes are given below. Please keep in mind that this is a construction site. Please watch your step for scattered hazards.

taupy inherits the symbolic approach from sympy. Since everything has to be declared before it can be used, you need to do so, too:

```python
from taupy import * 
from sympy import symbols
# Alternatively:
# from sympy.abc import a,b,c,...,x,y,z,A,B,C,...,X,Y,Z

a,b,c = symbols("a b c")

# An argument with premises a and b, conclusion ~c.
Argument(a&b,~c)

# A Debate consisting of two Arguments:
# The second argument attacks the first.
d,e = symbols("d e")
tau1 = Debate(Argument(a&b,~c), Argument(~d&e, ~a))
```

The third important class is Position. A Position is always relative to a debate:

```python
# A position for tau1 that allocates True to a and to b.
pos1 = Position(tau1, {a: True, b: True})

# Check whether the position is coheren:
pos1.is_coherent()

# Check whether it is complete, i.e. assigns True or False to any sentence in its Debate:
pos1.is_complete()

# Check whether it follows its "dialectical obligations", i.e. whether it is closed:
pos1.is_closed()
```

It's also possible to get more information about one Position or more:
```python
pos2 = Position(tau1, {d: False, e: True, a:False})

# What is the Hamming distance between pos1 and pos2?
hd(pos1, pos2)

# And their normalised agreement, i.e. HD / |Domain(pos)|?
# This will return a Fraction. If you can handle precision issues,
# you can do int(bna(pos1, pos2))
bna(pos1, pos2)

# What is the degree of justification for any of these Positions?
# (Again, you might want to do int(doj(pos1)) 
doj(pos1)
doj(pos2)
```

You can also get important information about the Debate itself. For example, its density, the
space of coherent and complete positions (sccp), and a representation of its argument map:

```python
tau1.density()
# Again, try int(tau1.density()) if you don't want Decimal output

# Give me the Debate's SCCP, in general exchange format that I can store in .graphml files:
tau1.sccp()

# Do the same for its argument map:
# map() here is a class method, it is something different entirely from the Python function map()
tau1.map()
```

The last two functions can be used for very rudimentary plotting using graph-tool:

```python
# Output the argument map of a Debate:
plot_map(tau1)

# Do the same for its SCCP:
plot_sccp(tau1)
```

This all leads to maybe the most important purpose of this package: Simulations! 

```python
# Initialise a Simulation with three empty positions:
sim1 = Simulation(positions=[{}, {}, {}])

# The sentence pool of a Simulation has to be pre-defined. You can do so with either variables
# in the global namespace, or with a new local namespace. The default creation is:
sim2 = Simulation(sentencepool="p:10")
# Create p0, p1,... p9 in a new local namespace. Accessible from the global namespace via
sim2.sentencepool[0], sim2.sentencepool[1], sim2.sentencepool[9]  

# Introduce a random argument to the Simulation.
# The argument is checked for uniqueness of premises and joint satisfiability with
# existing arguments:
introduce(sim1, introduce_random(sim1))

# Make the three positions respond to the latest introduction.
# Right now, there's only a very basic random reponse pattern:
response_random(sim1)

# It is possible to customise the length of introduced Arguments, i.e. the number of their premises:
sim3 = Simulation(argumentlength=2) # Introduce Arguments with two premises
sim3 = Simulation(argumentlength=[2,3]) # Arguments with two or three premises
```

## Functional structure

taupy
 - basic
   - core
     - Debate
     - Argument
   - positions
     - Position
 - analysis
   - agreement
     - mutual coherence
     - edit distance, Hamming distance
   - doj
   - inferential density
   - polarisation
 - simulation
   - agreement
   - argument introduction methods
   - belief updating rules
 - graphs
   - centrality/distance measures
   - visualisation
     - plot tau
     - plot sccp
