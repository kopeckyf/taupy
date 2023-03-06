Running a simulation
====================

taupy :py:obj:`Simulations` proceed through introductions or uncoverings of new arguments, agents' reactions to them, and sometimes also introductions of new items
to the sentence pool.

The simulation objects :py:obj:`taupy.Simulation` and 
:py:obj:`taupy.FixedDebateSimulation` have :py:meth:`run` methods
which automatically trigger these events.

.. automethod:: taupy.simulation.simulation.Simulation.run

.. automethod:: taupy.simulation.simulation.FixedDebateSimulation.run

These methods accept the following simulation termination conditions:

:py:attr:`max_density`: The maximum inferential density, determined by 
:py:func:`taupy.Base.density`, after which a simulation is terminated.

:py:attr:`max_steps`: Maximum number of argument introductions, uncoverings, and
sentence pool expansion events before the simulation is terminated. Can be set to 
a high value or to :py:obj:`float("inf")` so that only :py:attr:`max_density` has
effect.

:py:attr:`min_sccp`: The minimum extension of the set of coherent and complete
positions for the debate. If there are fewer positions in the SCCP at a debate 
stage, the simulation is terminated.

For example, let's start a simulation :py:obj:`s` until either a density of 0.8 
is reached or 200 argument and sentence introductions have been executed, 
whichever occurs first:

.. code:: python

    s.run(max_density=0.8, max_steps=200)
