Simulations
***********

.. code:: python

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