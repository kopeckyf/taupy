Setting up a simulation
=======================

Simulations are instances of a simulation class. There are multiple simulation
classes in :py:mod:`taupy` for different kinds of simulations. In the class 
:py:class:`taupy.Simulation` arguments are composed at each introduction step. In
the class :py:class:`taupy.FixedDebateSimulation`, argument maps are pre-compiled
and arguments are individually uncovered in each introduction step. 

There are many settings to the simulation classes, listed below, but not all of
them need to be configured for every simulation. Here is an example of a simulation
that runs largely on the defaults:

.. code:: python
    
	# Create 10 positions with strategy attack. These will receive random beliefs
	# as none are specified.
	my_population = [Position(
		debate=None, 
		introduction_strategy=strategies.attack
		) for _ in range(10)]

	# Set up a simulation with a sentence pool of 20, assign the population to it
	# and set an argument length to 2 or 3 premises.
	sim1 = Simulations(
		positions=my_population, 
		sentencepool="p:20", 
		argumentlength=[2,3]
	)
		
	# Run the simulation until an inferential density of 0.75 is reached.
	sim1.run(max_density=0.75)

Iterative argument introductions
--------------------------------

.. autoclass:: taupy.simulation.simulation.Simulation


Pre-compiled argument maps
--------------------------

.. autoclass:: taupy.simulation.simulation.FixedDebateSimulation

.. code:: python
 
    # The sentence pool of a Simulation has to be pre-defined. 
    # You can do so with either variables in the global namespace, 
    # or with a new local namespace (recommended). The default creation is:
    sim1 = Simulation(sentencepool="p:10")
    # Create p0, p1,... p9 in a new local namespace. 
    # Access them via:
    sim1.sentencepool[0], sim2.sentencepool[1], sim2.sentencepool[9]  
    
This would give us a debate without positions. Simulations without positions can
only behave un-directed. Introduced arguments can only be directed if there are
at least two positions, a `source` and a `target`.

.. code:: python

    # Initialise a Simulation with three empty positions:
    sim2 = Simulation(positions=[{}, {}, {}])
