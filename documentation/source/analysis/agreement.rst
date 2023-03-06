Agreement and distance
======================
The distance between two positions is always based on their differences in
truth-value assignments, and their agreement is closely related to this 
difference: if :math:`\delta` is a normalised distance function, then the 
normalised agreement of two positions :math:`x` and :math:`y` is given as 
:math:`1 - \delta(x, y)`.

The distance functions below accept pairs of agents and output the agreement or
distance of that pair. To obtain the differences among more than two positions, 
use :py:func:`difference_matrix` to obtain a square matrix of distances.  

.. autofunction:: taupy.analysis.polarisation.difference_matrix

Hamming distance
----------------
For positions that assign truth values to the same propositions, particularly 
for complete positions of the same debate, the Hamming distance is the most easy 
distance measure.
It simply counts the items that two positions evaluate differently. 

.. autofunction:: taupy.analysis.agreement.hamming_distance

The Hamming distance can be normalised to the number of proposition to which the
positions assign truth values (their “length”).

.. autofunction:: taupy.analysis.agreement.normalised_hamming_distance

Closely related to the Hamming distance is Betz' normalised agreement, or 
:py:func:`bna` for short. For two positions of equal domain, :math:`x` and 
:math:`y`, :math:`\text{bna}(x,y) = 1 - \text{HD}(x,y) / \text{len}(x)`. 

.. autofunction:: taupy.analysis.agreement.bna

Edit distance
-------------

The notion of difference and agreement is meaningful for positions of different
domains as well. The edit distance is equal to the minimal number of operations
that are necessary to transform one position into the other. Each operation is 
assigned to a weight, and the edit distance is calculated as a weighted sum of
the operations. There are three operations: switching of a truth value, adding
of a truth-value assignment, and deletion of one. The edit distance is generally
asymmetric if the weights are unequal.

.. hint:: When all operations in the edit distance have the same weight, the edit
          distance is a generalisation of the Hamming distance. For positions of
          equal domain, it then simplifies to the Hamming distance.

.. autofunction:: taupy.analysis.agreement.edit_distance

The edit distance can be normalised by first calculating the maximal distance
given the union of the positions' domains and the weights allocated to the 
operations. 

.. autofunction:: taupy.analysis.agreement.normalised_edit_distance

.. autofunction:: taupy.analysis.agreement.normalised_edit_agreement
