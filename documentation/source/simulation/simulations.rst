Setting up a simulation
=======================

Simulations are instances of a simulation class. There are multiple simulation
classes in :py:mod:`taupy` for different kinds of simulations. In the class 
:py:class:`taupy.Simulation` arguments are composed at each introduction step. 
In the class :py:class:`taupy.FixedDebateSimulation`, argument maps are 
pre-compiled and arguments are individually uncovered in each introduction step.


Examples
--------

A minimal example
^^^^^^^^^^^^^^^^^

Simulations that only introduce arguments, but have no agents that react to them
can be created with a call to :py:class:`Simulation` and leaving the 
:py:attr:`positions` to :py:obj:`None`. This would give us a debate without 
positions. Simulations without positions can only contain un-directed, random 
arguments. Introduced arguments can only follow a purposeful argumentation 
strategy if there are at least two agents in the population, a `source` and a 
`target`.

.. code:: python
 
    sim1 = Simulation(sentencepool="p:20")
    # Create p0, p1,... p19 in a new local namespace. Access them via:
    sim1.sentencepool[0], sim1.sentencepool[1], sim1.sentencepool[-1]  


A more realistic example
^^^^^^^^^^^^^^^^^^^^^^^^

There are many settings to the simulation classes, listed below, but not all of
them need to be configured for every simulation. Here is an example of a 
simulation that runs largely on the defaults:

.. code:: python
    
	# Create 10 positions with strategy attack. These will receive random beliefs
	# as none are specified.
	my_population = [Position(
		debate=None, 
		introduction_strategy=strategies.attack
		) for _ in range(10)]

	# Set up a simulation with a sentence pool of 20, assign the population to it
	# and set an argument length to 2 or 3 premises.
	sim2 = Simulation(
		positions=my_population, 
		sentencepool="p:20", 
		argumentlength=[2,3]
	)


Simulation types
----------------

Iterative argument introductions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: taupy.simulation.simulation.Simulation

Pre-compiled argument maps
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: taupy.simulation.simulation.FixedDebateSimulation
