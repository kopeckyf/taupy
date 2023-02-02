Inferential density
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
