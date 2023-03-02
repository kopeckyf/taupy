Simulations
***********

Debates and Positions are static objects: they describe arguments and an agent's
belief system at one point in time. Simulations track dynamical aspects of 
debates and belief systems.

The simulated world consists of a sentence pool and arguments on these sentences. 
Agents have a multi-dimensional belief system in terms of Positions. The Simulations
progress by introducing arguments, possibly according to an argumentation strategy
assigned to agents. Agents update their belief systems in response to argument 
introductions according to a pre-defined update strategy. The simulation terminates
when the desired inferential density is reached or the desired number of arguments 
has been introduced.

1. For the introduction event, two random positions are selected. If there are none,
   a random argument is inserted. If both `source` and `target` positions can be found, an argument is introduced according to the introduction strategy of the source. If no combinations of premises can be found that fit this stragegy, the simulation stops.
   
2. The update mechanism is then applied to *all* positions. Details on these mechanisms can be found in the submodule :py:mod:`taupy.simulation.update`.

.. toctree::
   :hidden:

   simulations
   populations
   update
   experiments
   evaluation
