Polarisation
============

Identifying a population as polarised depends on a measure of polarisation as 
there are many different notions of “polarisation” ([Bramson2016]_).
:py:mod:`taupy` implements many of the measures identified by Bramson et al., but
in a definition that is adapted to the belief systems in the theory of 
dialectical structures.

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
