Diversity
=========

Functions to measure diversity among deliberating agents. Interestingly, many
functions in the module have a common abstract ancestor function 
([Tuomisto2010]_), but are implemented here in a rather pedestrian way for 
simplicty.

Shannon index and derivatives
-----------------------------

.. autofunction:: taupy.analysis.diversity.Shannon_index

.. autofunction:: taupy.analysis.diversity.normalised_Shannon_index

Simpson index and derivatives
-----------------------------

.. autofunction:: taupy.analysis.diversity.Simpson_index

.. autofunction:: taupy.analysis.diversity.inverse_Simpson_index

.. autofunction:: taupy.analysis.diversity.Gini_Simpson_index

Attribute diversity
-------------------

.. autofunction:: taupy.analysis.diversity.attribute_diversity_page

.. autofunction:: taupy.analysis.diversity.normalised_attribute_diversity_page