Debate analysis
***************

In the last step of the tutorial, we constructed a simple debate containing two 
arguments. `taupy` can analyse its debate object in a variety of ways, by 
measuring:

1. distances between positions and agreement between them
2. degrees of justification
3. dialectical density
4. different concepts of polarisation
5. graph objects


Measuring distances and agreement
=================================
Let us continue the debate from the previous step:

.. code:: python
   
   tau1 = Debate(Argument(a&b,~c), Argument(~d&e, ~a))
   pos1 = Position(tau1, {a: True, b: False, c: True})
   pos2 = Position(tau1, {d: False, e: True, a: False})

We can now check the Hamming distance and the unweighted edit distance between
`pos1` and `pos2`, along with their normalised agreement:   

.. code:: python

   # What is the Hamming distance between pos1 and pos2?
   hd(pos1, pos2)
   
   # Check the unweighted edit distance
   edit_distance(pos1, pos2)

   # And their normalised agreement, i.e. HD / |Domain(pos)|?
   # This will return a Fraction. If you can handle precision issues,
   # you can do int(bna(pos1, pos2))
   bna(pos1, pos2)
   
`bna()` measures the normalised agreement between two complete positions.

Measuring degrees of justification (DOJ)
========================================

.. admonition:: Background reading
   :class: seealso 
   
   [Betz2012]_ 

Unconditional DOJs
------------------

In TDS, the degree of justification of a set of propositions is defined by
the relation

.. math::
    
    \text{doj}(P)_\tau := \frac{\text{Number of complete and coherent positions on $\tau$ that extend $P$}}{\text{Number of complete and coherent positions on $\tau$}}
    
A different way to understand this would be in terms of probability: if all 
complete and coherent positions in a debate :math:`\tau` were equally likely of
being selected, then what is the probability that the set of propositions :math:`P`
will be true according to a randomly chosen position? 
    
The DOJ of a position `pos` is defined as the DOJ of the propositions that `pos`
opines on. For these propositions :math:`p_i`, :math:`p_i` is added to the set if `pos`
assigns True to :math:`p_i`, but :math:`\neg p_i` is added if `pos` assigns False to 
:math:`p_i`.

.. code:: python

   # What is the degree of justification for any of these Positions?
   doj(pos1)
   doj(pos2)
   
.. tip:: :func:`taupy.doj` returns a fraction. If you want to use integers instead,
         call :code:`int(doj())`.
         

Conditional DOJs
----------------

The conditional DOJ adds a condition to the equation. Let :math:`C` be a set of 
propositions that form the condition. Then 

.. math::
    
    \text{doj}(P|C)_\tau := \frac{\text{Number of complete and coherent positions on $\tau$ that accept $C$ and extend $P$}}{\text{Number of complete and coherent positions on $\tau$ that accept $C$}}
    
In `taupy`, a conditional DOJ is calculated with the `conditional` argument: 

.. code:: python

   # What is the degree of justification for pos1, conditional to pos2?
   doj(pos1, conditional=pos2)
   
.. warning:: In conditional DOJs, both the set of propositions :math:`P` 
             and the set of conditions :math:`C` must have the same `debate`.
             
             
Dialectical density
===================

Debate objects have a method :meth:`density()`. Dialectical density is a measures
of how much the arguments in a debate have constrained the space of coherent 
positions. A debate in which the arguments impose rather few constraints on the
available complete and coherent positions will have a low density; a debate in
which this influence is high, the debate's density will be high as well. However,
while the density generally rises with number of arguments, not every argument
renders a previously coherent position incoherent. And so, not every argument
contributes to density equally, and some won't change it at all. Density offers
a time-indepent measure of *progress* in debates, an alternative to the number
of introduced arguments.

.. code:: python

   tau1.density()

.. tip:: Density is returned as a fraction. If you prefer integers, try 
         :code:`int(tau1.density())`.
         
.. admonition:: Background reading
   :class: seealso 
   
   [Betz2013]_ (pages 44-49)
   

Measures of polarisation
========================

.. admonition:: Background reading
   :class: seealso 
   
   [BramsonEtAl2016]_



Graph objects induced by debate objects
=======================================


You can also get important information about the Debate itself. For
example, its density, the space of coherent and complete positions
(sccp), and a representation of its argument map:

.. code:: python

   # Give me the Debate's SCCP, in general exchange format that I can store in .graphml files:
   tau1.sccp()

   # Do the same for its argument map:
   # map() here is a class method, it is something different entirely from the Python function map()
   tau1.map()

You can then use the objects returned by the class methods `sccp()` and `map()` to 
plot them using networkx, graph-tool, or similar packages.

.. important:: taupy is not aimed to be a visualisation tool. If you are looking for 
               a capable argument visualisation tool, have a look at `Argdown <https://argdown.org/>`

References
==========

.. [Betz2012] Betz, Gregor. 2012. On degrees of justification. Erkenntnis 77.
              pp. 237--272. DOI: <https://doi.org/10/bkng95>

.. [Betz2013] Betz, Gregor. 2013. Debate dynamics. How controversy improves
              our beliefs. Springer. DOI: <https://doi.org/10/d3cx>
              
.. [BramsonEtAl2016] Bramson, Aaron et al. 2016. Disambiguation of social 
   polarization concepts and measures. The Journal of Mathematical Sociology 
   40(2), pp. 80--111. DOI: <https://doi.org/10/d3kn>
