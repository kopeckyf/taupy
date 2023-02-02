Agreement and distance
======================
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
