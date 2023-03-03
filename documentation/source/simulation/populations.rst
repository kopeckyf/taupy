Setting up a population
=======================

A debate can progress without any agents present. In this case, arguments will be
inserted to, or uncovered from, the argument map until a stopping criterion is used.
Simulations in which agents update their belief systems need to be initialised with
a list of positions.

When simulations are initialised with a population, the agents from this population
update their belief systems in response to argument introductions and sentence
pool expansions. The simulation objects have a :py:attr:`Simulation.positions` 
attribute, which is a list of populations in which the $i$th element stores the
population at the $i$th simulation step. The initialised population is stored in
the first element, :py:attr:`Simulation.positions[0]`.

Populations are lists of positions
----------------------------------

The initial population needs to be generated as a list of 
:py:obj:`taupy.Position` objects:

>>> my_population = [Position() for _ in range(10)]

The agents' behaviour in argument introductions can be controlled using the 
:py:attr:`introduction_strategy` attribute.

>>> my_population = [Position(debate=None, introduction_strategy=strategies.fortify for _ in range(10)]

A population can consist of agents with different argumentation strategies (see
the :py:mod:`taupy.simulation.strategies` module for pre-defined strategies. 
Custom argumentation strategies are also accepted):

>>> fortify_positions = [Position(debate=None, introduction_strategy=strategies.fortify for _ in range(5)]
>>> convert_positions = [Position(debate=None, introduction_strategy=strategies.convert for _ in range(5)]
>>> my_population = fortify_positions + convert_positions 

When you initialise positions like this, they will be assigned random thruth-value
attributions during the simulation initialisation. You can also generate a
population with custom beliefs. For example, these could be bi-polarised:

.. code-block:: python

	pos_template_1 = {
		symbols("p0"): True, symbols("p1"): True, symbols("p2"): True,
		symbols("p3"): True, symbols("p4"): True, symbols("p5"): True
	}
        
	pos_template_2 = {
		symbols("p0"): False, symbols("p1"): False, symbols("p2"): False, 
		symbols("p3"): False, symbols("p4"): False, symbols("p5"): False
	}
	
	pop_part_1 = [Position(None, pos_template_1, introduction_strategy=strategies.convert) for _ in range(10)]
	pop_part_2 = [Position(None, pos_template_2, introduction_strategy=strategies.undercut) for _ in range(10)]
	
	my_polarised_pop = pop_part_1 + pop_part_2

Argumentation strategies
------------------------

.. automodule:: taupy.simulation.strategies
