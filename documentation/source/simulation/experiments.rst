Experiments: Simulations in parallel
====================================

As simulations involve random processes it is often necessary to inspect multiple
simulation runs to ensure one didn't end up with an outlier. The 
:py:func:`experiment` function can process any number of simulations in parallel.

.. warning::
	
	Calling :py:func:`experiment` will start the requested simulations
	immediately. By default, it will use all available CPUs on your system to
	do so. Depending on the set-up, this can keep your machine busy for quite
	some time. You can employ less CPUs by changing the :py:attr:`max_workers` 
	setting in the :py:attr:`executor` argument.
	
.. autofunction:: taupy.simulation.simulation.experiment

.. code:: python
    
    # First, create 10 positions with strategy random
    positions = [Position(debate=None, introduction_strategy=strategies.random) for _ in range(10)]
    
    # Run 4 simulations in an experiment (multi-threaded!):
    my_experiments = experiment(n=4,
                                simulations={"positions": positions,
                                             "sentencepool": "p:10",
                                             "argumentlength": [2,3]},
                                runs={"max_density": 0.8,
                                      "max_steps": 200}
                                )

This creates an object :py:obj:`my_experiments` with four elements: :py:obj:`my_experiments[0]`
contains the first simulation, the second is in :py:obj:`my_experiments[1]`, etc.

The dictionary in the :py:attr:`simulations` argument contains the arguments for 
creation of the :py:obj:`Simulation` objects. For example, the above call to 
:py:func:`taupy.experiment` creates simulation object :py:obj:`s` that look like 
this:

.. code:: python

    s = Simulation(positions=positions, sentencepool="p:10", "argumentlength"=[2,3])
    

And the directives in the dictionary :py:attr:`runs` are arguments to the method
:py:meth:`Simulation.run()` which is called by the experiments. The settings 
above are equivalent to:

.. code:: python

    s.run(max_density=0.8, max_steps=200)
    

