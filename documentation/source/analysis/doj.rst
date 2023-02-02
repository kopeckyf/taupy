Degrees of justification
========================

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
