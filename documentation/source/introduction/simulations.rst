Simulations
***********

There are properties of debates that can't be understood from an individual debate
stage, but only become apparent when a debate's evolution time is considered. 
Debates may converge toward agreement, or they may diverge and even form *deep
disagreements*. They can also polarise or depolarise, and some debates may become
more or less diverse and more or less veracious.

Events
======

A taupy :py:obj:`Simulation` has two events: the (1) introduction of a new argument and
(2) reaction of the positions in the debate to this new debate stage. Both events 
trigger at each turn of the simulation.

.. note:: A third kind of event, enlargement of the sentence pool, will be available
          in a future taupy version.
          
1. For the introduction event, two random positions are selected. If there are none,
   a random argument is inserted. If both `source` and `target` positions can be found,
   an argument is introduced according to the introduction strategy of the source. If
   no combinations of premises can be found that fit this stragegy, the simulation stops.
   
2. The update mechanism is then applied to *all* positions. Details on these mechanisms 
   can be found in the submodule :py:mod:`taupy.simulation.update`.
   
Setting up pools of positions and propositions
==============================================

Other than in static debates, taupy simulations usually don't take their propositions
from the public namespace (this would populate it rather quickly!). Each :py:obj:`Simulation`
has its own private sentence name space. A good way to generate it is to use 
`sympy`'s :code:`"p:n"` syntax, where :code:`n` is the number of propositions 
one needs:

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

Inserting arguments manually
============================

Now that a simulation is set-up, we can introduce an argument into the debate.
We need the submodule :py:mod:`taupy.simulation.strategies` to get the info that 
taupy needs to create an argument based on a strategy.
 
.. code:: python

    import taupy.simulation.strategies as strategies
    # Introduce a random argument to the Simulation.
    # The argument is checked for uniqueness of premises 
    # and joint satisfiability with existing arguments:
    introduce(sim1, strategy=strategies.random)
 
You can then let all the positions respond to the newly introduced argument:

.. code:: python

    # Make the three positions respond to the latest introduction.
    response(sim1, method="closest_coherent")
    
.. warning:: The :py:obj:`method` argument will certainly change once there are
             more update strategies besides `random` and `closest_coherent`.

Running experiments that insert arguments automatically
=======================================================

There isn't much fun in entering every argument yourself: debate simulations can
take hundreds of steps before coming to an end. Also, for most research questions
you probably want to run more than one simulation to make sure you haven't ended up
with an outlier. The :py:func:`taupy.experiment` function provides for all of these
needs.

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

The dictionary in the `simulations` argument contains the arguments for creation of the 
:py:obj:`Simulation` object. So the above call to :py:func:`taupy.experiment` creates
simulation object :py:obj:`s` that look like this:

.. code:: python

    s = Simulation(positions=positions, sentencepool="p:10", "argumentlength"=[2,3])
    

And the directives in the dictionary `runs` are arguments to the method `Simulation.run()`
which is called by the experiments. So the setting above are equivalent to:

.. code:: python

    s.run(max_density=0.8, max_steps=200)
    
For each simulation :py:obj:`s` of the four generated by the experiment.

.. seealso::  To learn more about the configuration options, have a look at the submodule 
              :py:mod:`taupy.simulation` and the functions documented there. There are also two
              Tutorials which show useful simulation experiments.
