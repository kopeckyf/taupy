Centrality
----------

A population can be interpreted as a graph in which the individual agents make
up the nodes of the graph, and the edge weights are determined by the distance
between belief systems. Agents can inhibit the centre of a graph or be far 
removed at the fringes. The normalised closeness centrality indicates this 
position for a single agent in a population relative to a distance measure. 
In the graph below, the top position has a low distance of 1 to each of the 
others, but the others have a higher distance toward each other. The top agent
thus is the most central node. 

.. image:: ncc-illustration.svg
   :align: center
   :class: only-light
   
.. image:: ncc-illustration-dark.svg
   :align: center
   :class: only-dark
   
.. hint:: There can be multiple, far removed agents with maximum NCC in a 
          population. In other words, a population graph can have multiple 
          graph centres.

.. autofunction:: taupy.analysis.agreement.ncc
