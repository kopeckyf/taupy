Debates
*******

Debates are sets of arguments
=============================

A debate in the theory of dialectical structures is a set of arguments on which 
two relations are defined: support and defeat. Formally, a debate is a tuple 
:math:`\tau = \left< T, A, U\right>`, where :math:`T` is the set of arguments, 
:math:`A` the pairs of arguments that fulfil the support relation, and :math:`U` 
the pairs of arguments that fulfil the support relation.

Relations between arguments in a debate
=======================================
The defeat and support relation in TDS are defined as follows: An argument 
:math:`a\in T` defeats another argument :math:`b\in T` if the conclusion of 
:math:`a` is equivalent to the negation of a premise in :math:`b`. An argument 
:math:`a\in T` supports another :math:`b\in T` if the conclusion of :math:`a` is 
equivalent to one of the premises in :math:`b`.

In taupy, you don't have to input these relations manually – and in fact, you 
can't. They are determined automatically from the arguments in your input. In the
map below, supports between arguments are visualised with solid edges, and 
defeats through dashed edges.

.. image:: argument_map.svg
   :align: center
   :class: only-light
   
.. image:: argument_map_dark.svg
   :align: center
   :class: only-dark

Debate objects
==============

In :py:mod:`taupy`, debates are instances of the :py:class:`taupy.Debate` class. 

.. autoclass:: taupy.basic.core.Debate
   
A :py:class:`Debate` is composed of arguments. These do not necessarily exhibit 
any relation. When a debate is initialised, its arguments are given as a 
comma-separated list. Any number of arguments can be passed to an 
:py:class:`Debate` object.

.. code:: python  

   from taupy import Argument, Debate
   from sympy import symbols
   a, b, c, d, e = symbols("a b c d e")
   tau1 = Debate(Argument(a&b, ~c), Argument(~d&e, ~a))

:py:obj:`tau1` is a debate with two arguments. The second :py:obj:`Argument(~d&e, 
~a)` defeats the first :py:obj:`Argument(a&b, ~c)`.
