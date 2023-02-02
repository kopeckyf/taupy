Positions
*********

Positions are belief sytems of agents
=====================================

Arguments are relations between propositions: if the premises were true, the
conclusion would be as well. Agents can accept arguments as valid without 
agreeing to the premises. The mere existence of an argument does not force an
agent to assert the conclusion if it does not accept one or more of the premises.

The theory of dialectical structures represents belief systems of agents as 
mappings from the propositions discussed in a debate to truth values. This means 
that positions are always relative to a debate. 

Let us look at a debate :math:`\tau_1` with five propositions: a, b, c, 
d and e, and a position :math:`\text{Pos}_1` that assigns truth values to these
propositions.

.. math::
   \begin{align*}
   \tau_1 = &  ((a\land b) \implies \neg c) \\
          &   \land (( \neg d \land e) \implies \neg a)\\
          \\
   \text{Pos}_1 = &  \left\{ \begin{array}{l}
                    a \to \text{True}\\
                    b \to \text{False}\\
                    c \to \text{True}\\
                    d \to \text{True}\\
                    e \to \text{False}\\
                    \end{array} \right\}
   \end{align*}

In :py:mod:`taupy`, positions are input with as instances of :py:class:`Position`.

.. autoclass:: taupy.basic.positions.Position

The above example can be typed like this:

.. code:: python  

   from taupy import Argument, Debate, Position
   from sympy import symbols
   a, b, c, d, e = symbols("a b c d e")
   tau1 = Debate(Argument(a&b, ~c), Argument(~d&e, ~a))
   pos1 = Position(tau1, {a: True, b: False, c: True, d: True, e: False}) 
   
Properties of positions
=======================

Completeness
------------
A position does not need to assign a truth value to every sentence in the pool. A position that does not, 
as the above example :math:`p`, is called *partial*. A *complete* position assigns a truth value to every
proposition in the debate. 

.. automethod:: taupy.basic.positions.Position.is_complete

In `taupy`, positins are a third kind of object: a `Position`. Positions are always relative to a debate,
which should be given as the first argument when creating a new `Position` object. The truth-value assignment
(TVA) is given as a Python dictionary in the second argument:

.. code:: python

   pos1 = Position(tau1, {a: True, b: False, c: True})
   # Check whether it is complete, i.e. assigns True or False to any sentence in its Debate:
   pos1.is_complete()

Positions can be complete or partial, and they have two more important properties: coherence and closedness.

Closedness
----------

A position is closed if it follows its dialectical obgliations: if a position 
assigns True to all premises in an argument, it must also assign True to the 
conclusion.

.. autofunction:: taupy.basic.positions.closedness

.. automethod:: taupy.basic.positions.Position.is_closed

Coherence
---------
There are two ways to express coherence for a position relative to a debate:

1. The position (a) assigns identical truth values to sentences that are 
   equivalent give the debate and complementary truth values to incompatible
   ones and (b) does not contradict its inferential obligations, i.e. if it 
   accepts all premises of an argument, it can not reject the conclusion.
2. The position satisfies the Boolean formula that represents the debate. In
   other words, if :math:`\text{SAT}(\tau)` returns the set of satisfying 
   assignments of the Boolean formula for the debate :math:`\tau`, then a 
   position :math:`\text{pos}` is coherent just in case :math:`\text{pos} \in 
   \text{SAT}(\tau)`.
   
.. note:: Coherence does not imply closedness. Under condition (1b), a coherent
   position is only required not to contradict its inferential obligations. But
   a coherent position can still not follow some of them, e.g. by being a partial
   position and not assigning a value to the conclusion, or by suspending 
   judgement on it.
   
   Coherence and completeness jointly imply closedness.
   
.. automethod:: taupy.basic.positions.Position.is_coherent

.. code:: python

   pos1 = Position(Debate(Argument(a&~b, c)), {a: True, b: False, c: False})
   # Will return False:
   pos1.is_coherent()
   
The set of coherent and complete positions
==========================================
A central concept to the theory of dialectical structures is the collection of
all positions that are coherent and complete (and thus closed) given a debate.

Given a debate :py:obj:`tau`, this set can be obtained with 
:code:`taupy.satisfiability(tau, all_models=true)`.

.. autofunction:: taupy.basic.utilities.satisfiability

When interpreted as a graph, this set is called the *space of coherent and 
complete positions*, or SCCP, often expressed by the Greek letter Gamma 
(:math:`\Gamma`). The SCCP can yield insights about the debate itself.

.. automethod:: taupy.basic.core.Debate.sccp

.. code:: python

   tau1 = Debate(Argument(a&~b, c))
   tau1.sccp()

