:hide-toc:

Welcome to taupy's documentation!
#################################

:py:mod:`taupy` is a Python package for the study of dialectical structures. 

A dialectical structure is an abstract representation of a debate, including 
its arguments and the belief systems agents adopt in light of the arguments. 
The Greek letter tau (τ) is used in the theory of dialectical structures to 
describe its fundamental variable: A triple consisting of a set of arguments 
together with a support and a defeat relation. Hence the name for this package.

.. seealso::

   Introductions to the theory of dialectical structures can be found in 
   [Betz2013]_, pp. 33–36 (recommended general introduction) and
   [Betz2009]_ (more technical, logic-oriented).  

.. note:: 

   This package is not a debate reconstruction tool: it does not offer tools for
   diagramming or other modes of visualisation. For these purposes, please have a 
   look at `Argdown <https://argdown.org>`_.


.. toctree::
   :hidden:
   :caption: User guide
   
   installation/index
   basic/index
   analysis/index
   generators/index
   simulation/index
   
   references
   genindex
   
.. toctree::
   :hidden:   
   :caption: Examples
   
   tutorials/plotting-sccp
   tutorials/agreement
