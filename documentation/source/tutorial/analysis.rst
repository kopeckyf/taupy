Debate analysis
***************


Measuring distances and agreement
=================================


.. code:: python

   pos2 = Position(tau1, {d: False, e: True, a:False})

   # What is the Hamming distance between pos1 and pos2?
   hd(pos1, pos2)

   # And their normalised agreement, i.e. HD / |Domain(pos)|?
   # This will return a Fraction. If you can handle precision issues,
   # you can do int(bna(pos1, pos2))
   bna(pos1, pos2)

Measuring degrees of justification (DOJ)
========================================

.. code:: python
   # What is the degree of justification for any of these Positions?
   # (Again, you might want to do int(doj(pos1)) 
   doj(pos1)
   doj(pos2)


You can also get important information about the Debate itself. For
example, its density, the space of coherent and complete positions
(sccp), and a representation of its argument map:

.. code:: python

   tau1.density()
   # Again, try int(tau1.density()) if you don't want Decimal output

   # Give me the Debate's SCCP, in general exchange format that I can store in .graphml files:
   tau1.sccp()

   # Do the same for its argument map:
   # map() here is a class method, it is something different entirely from the Python function map()
   tau1.map()

The last two functions can be used for very rudimentary plotting using
graph-tool:

.. code:: python

   # Output the argument map of a Debate:
   plot_map(tau1)

   # Do the same for its SCCP:
   plot_sccp(tau1)

This all leads to maybe the most important purpose of this package:
Simulations!