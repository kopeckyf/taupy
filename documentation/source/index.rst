:hide-toc:

Welcome to taupy's documentation!
#################################

taupy is a Python package for the study of dialectical structures. 

A dialectical structure is an abstract representation of debates, including their 
arguments and relations between them as well as positions that agents take in 
light of the arguments. The Greek 
letter tau (τ) is used in the theory of dialectical structures to describe its 
fundamental variable: A triple consisting of a set of arguments together with the
support and defeat relations among the arguments. Hence the name for this package.

.. seealso::

   Introductions to the theory of dialectical structures can be found in 
   [Betz2009]_ (more technical, logic-oriented) and [Betz2013]_, pp. 33–36 
   (recommended general introduction).  

This package is not a debate reconstruction tool, and has only rudimentary tools 
for visualisation. For these purposes, you could have a look at 
`Argdown <https://argdown.org>`_.

If you'd like to report an issue or file a feature request, please open an
issue in `taupy's GitHub repository <https://github.com/kopeckyf/taupy>`_. 
There's also a change log and release history on GitHub.

Besides the content in this documentation, there are some special pages: 
The :ref:`genindex` and the :ref:`modindex` and the :ref:`modules`.

.. toctree::
   :hidden:
   :caption: User guide
   
   installation/index
   basic/index
   analysis/index
   generators/index
   simulation/index
   
   references
   
.. toctree::
   :hidden:   
   :caption: Examples
   
   tutorials/plotting-sccp
   tutorials/agreement
