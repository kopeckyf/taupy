Inferential density
===================

Inferential density is a measures of how much the arguments in a debate have 
constrained the space of coherent positions, and by that the choice of admissible
belief systems for participants of a debate. 

Consider how the debate consisting of just one argument, :math:`(a\land b) 
\implies c` has :math:`2^3-1` coherent and complete truth-value assignments. The
one that is missing assigns False to :math:`c` but True to :math:`a` and 
:math:`b`. Betz ([Betz2013]_, p. 44) gives a formula for calculating the density 
of a debate :math:`\tau`, :math:`D(\tau)` with sentene pool of length :math:`n`
and a space of complete on coherent positions :math:`\Gamma(\tau)`:

.. math::
   D(\tau) := \frac{n-\log_2 (|\Gamma(\tau)|)}{n}


Density offers a time-indepent measure of progress in debates, a reliable 
alternative to the number of introduced arguments. A debate in which the
arguments impose rather few constraints on the available complete and coherent
positions will have a low density; a debate in which this influence is high, the
debate's density will be high as well. However, while the density generally rises 
with number of arguments, not every argument renders a previously coherent 
position incoherent. And so, not every argument contributes to density equally,
and some won't change it at all. 

.. automethod:: taupy.basic.core.Base.density

.. tip:: Density is returned as a fraction. If you prefer integers, try 
         :code:`int(tau1.density())`.
         
.. seealso:: 
   Betz discusses this concept in more depth in [Betz2013]_ (pages 44-49).