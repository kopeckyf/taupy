Degrees of justification
========================

A degree of justification (DOJ) quantifies how justified a truth-value assignment
is in light of a debate. A DOJ always lies in the interval [0, 1] – and they can
be treated as probabilities in the sense that the DOJ measure fulfils the 
Kolmogorov axioms ([Betz2012]_, Theorem 6). 

.. seealso:: The concept was introduced to the theory of dialectical structures
             in [Betz2012]_. 
             
.. autofunction:: taupy.analysis.doj.doj

.. tip:: :func:`taupy.doj` returns a fraction. If you want to use integers instead,
         call :code:`int(doj())`.

Unconditional DOJs
------------------

Let :math:`P` be a (partial) position in the debate :math:`\tau` and 
:math:`\Gamma(\tau)` the space of coherent and complete positions on 
:math:`\tau`. Then, the degree of justification of :math:`P` in :math:`\tau` is 
defined as follows.

.. math::
    
    \text{doj}(P)_\tau := \frac{
    	\left|\left\{\gamma \in \Gamma_\tau | P \subseteq \gamma\right\}\right|}
    	{|\Gamma_\tau|}
    
The DOJ of a position :math:`P` in a debate is equal to the proportion of 
positions in the debate's SCCP that extend :math:`P`, or have its truth-value 
assignments as a part. One can also understand this in terms of probability: if 
all complete and coherent positions in a debate :math:`\tau` were equally likely 
of being drawn, then what is the probability that the set of propositions 
:math:`P` would be true according to a randomly chosen position? 

.. note:: The DOJ of an incoherent position always equals zero. The DOJ of a 
	  complete position equals :math:`1/|\Gamma_\tau|`, since there is 
	  exactly one item in the SCCP that extents that position – and this is
	  the position itself. This means that DOJs are most informative for 
	  coherent partial positions.
   
Conditional DOJs
----------------

We can not only ask the question of how well a position is justified given a 
debate simpliciter, but also how well it would be justified if some statements 
in the debate were taken for granted. Let :math:`C` be a set of propositions 
relative to which the justification of :math:`P` should be evaluated. 

.. math::
    
    \text{doj}(P|C)_\tau := \frac{\{|\gamma\in\Gamma_\tau \cap C | P \subseteq \gamma\}|}
    				 {|\{\gamma\in\Gamma_\tau \cap C\}|}
    
In `taupy`, a conditional DOJ is calculated with the `conditional` argument: 

.. code:: python

   # What is the degree of justification for pos1, conditional to pos2?
   doj(pos1, conditional=pos2)
   
.. warning:: In conditional DOJs, both the set of propositions :math:`P` 
             and the set of conditions :math:`C` must have the same `debate`.
