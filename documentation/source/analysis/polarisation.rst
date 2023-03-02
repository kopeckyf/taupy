Polarisation
============

Polarisation has many meanings. Identifying a populations as polarised depends, 
to some degree, on the measure of polarisation. Bramson et al. ([Bramson2016]_)
review some of these measures, and :py:mod:`taupy` implements many of these 
measures in a definition that is adapted to the belief systems its agents have.

Measures without clustering
---------------------------

.. autofunction:: taupy.analysis.polarisation.spread

.. autofunction:: taupy.analysis.polarisation.pairwise_dispersion

Meaures with clustering
-----------------------

.. autofunction:: taupy.analysis.polarisation.group_divergence

.. autofunction:: taupy.analysis.polarisation.group_consensus

.. autofunction:: taupy.analysis.polarisation.group_size_parity

.. autofunction:: taupy.analysis.polarisation.coverage_of_clustering
