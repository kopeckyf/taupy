Evaluation
==========

The :py:class:`Evaluation <taupy.simulation.evaluation.Evaluation>` class 
provides methods for analysing many debate stages, positions, and storing that
information in a combined data table. It performs most of its operations 
concurrently and gives a performance advantage on machines with many processors.
All measures described in :ref:`Analysis & measurement` can be applied to 
:py:class:`Evaluation` objects.

Setting up an Evaluation object
-------------------------------
.. autoclass:: taupy.simulation.evaluation.Evaluation

Viewing results
---------------

All measurement functions from the evaluation module are configured to add 
columns to a shared :py:class:`pandas.DataFrame` stored in 
:py:obj:`Evaluation.data`.

.. code-block:: python

    e = Evaluation()
    # View the DataFrame
    e.data
    # Since e.data is a pandas DataFrame, all DataFrame operations can be used:
    e.data.to_csv("myexport.csv")
    
An :py:obj:`Evaluation.data` table is structured like this:

== == ======= ==========
.. .. density dispersion
== == ======= ==========
0  0  0.02324 0.29561402
0  1  0.07451 0.30156791
0  2  0.08462 0.30196067
0  3  0.09880 0.30971113
== == ======= ==========

The first two columns indicate the :py:obj:`pandas.MultiIndex` for the table. 
The first column corresponds to the simulation number within the experiment, and
the second column to the debate stage within the simulation. The remaining 
columns are inserted by the :py:class:`Evaluation` class methods described 
below. 
    
A minimal example
-----------------

Suppose you have run an experiment with iterative argument introductions and 
want to analyse the density and pairwise dispersion of each debate stage.

.. code:: python
    
    # First, create 10 positions with strategy random
    my_population = [Position(debate=None, introduction_strategy=strategies.random) for _ in range(10)]
    
    # Run 4 simulations in an experiment:
    my_experiments = experiment(
        n=4,
        simulations={"positions": my_population, "sentencepool": "p:10", "argumentlength": [2,3]},
        runs={"max_density": 0.8, "max_steps": 200}
        )
    
    # Create an Evaluation object
    e = Evaluation(
        debate_stages=my_experiments, 
        list_of_positions=[e.positions for e in my_experiments]
        )
    # Add a density column to the data
    e.densities()
    # Add a column with pairwise dispersion measurements to the data
    e.dispersions()
    
The resulting :py:obj:`e.data` table is intended for further data analysis, such
as statistics or plotting. These operations will be performed outside of 
:py:mod:`taupy`, in modules such as :py:mod:`numpy` or :py:mod:`seaborn`.

Adding data to an Evaluation object
-----------------------------------

Shortcut functions
^^^^^^^^^^^^^^^^^^

These functions are shortcuts to the functions explained in more detail below. 

.. automethod:: taupy.simulation.evaluation.Evaluation.densities
.. automethod:: taupy.simulation.evaluation.Evaluation.dispersions
.. automethod:: taupy.simulation.evaluation.Evaluation.agreement_means

Measures that only analyse debate stages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: taupy.simulation.evaluation.Evaluation.debate_stage_analysis

.. autofunction:: taupy.simulation.evaluation.densities_of_debate_stages
.. autofunction:: taupy.simulation.evaluation.sccp_extension
.. autofunction:: taupy.simulation.evaluation.progress


Measures that only analyse positions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: taupy.simulation.evaluation.Evaluation.position_analysis

.. autofunction:: taupy.simulation.evaluation.dispersions_between_positions
.. autofunction:: taupy.simulation.evaluation.mean_agreement_between_positions

Measures that rely on clustering
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: taupy.simulation.evaluation.Evaluation.generate_clusters

.. automethod:: taupy.simulation.evaluation.Evaluation.group_divergence
.. automethod:: taupy.simulation.evaluation.Evaluation.group_consensus

.. automethod:: taupy.simulation.evaluation.Evaluation.clusters_analysis
