Introduction to taupy and its basic ontology
*********************************************

taupy is a Python package for studying the theory of dialectical structures (TDS) in Python.

What is TDS?
============

The theory of dialectical structures is a member of the argumentation frameworks family of theories.
In the theory, real-world arguments can be reconstructed. They are then represented as premise-conclusion
structures. TDS can also be used to represent arguments only symbolically - that is, the premise-conclusion
structures are not filled with meaningful sentences, but take sentence variables instead. 

TDS can be used to measure important values of debates. For example, we can ask how well individual
sentences are justified, from an argumentative point of view, in a debate. But we can also determine
the level of agreement between diverse positions in a debate, study argument introduction strategies and 
belief updating rules as kinds of intentional behaviour by artificial agents. We can also measure 
fragmentations of positions in debate and measure polarisation.

The basic ontology of TDS and its implementation in taupy
=========================================================

TDS understands a debate to be a set of arguments on which two relations are defined: support and attack.
Formally, a debate is a tuple :math:`\tau = \left< T, A, U\right>`, where :math:`T` is the set of 
arguments, :math:`A` the pairs of arguments that fulfil the attack relation, and :math:`U` the pairs of
arguments that fulfil the support relation.

Arguments
---------
TDS defines arguments to be premise-conclusion structures. This means that any argument has a set of 
premises :math:`\left\{ a_1, a_2, ... a_n \right\}`, a rule of inference :math:`r` and a conclusion :math:`c`.
In taupy, we don't implement the rule of inference since we assume that any argument is valid. Then, the 
logical meaning of an argument is that of a logical implication: :math:`\left\{ a_1, a_2, ... a_n \right\} \to c`.

TDS also provides for theses, which are single sentences.

Relations between arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^
The attack and support relation in TDS are defined as follows: An argument :math:`a\in T` attacks another
argument :math:`b\in T` if the conclusion of :math:`a` is equivalent to the negation of a premise in :math:`b`.
An argument :math:`a\in T` supports another :math:`b\in T` if the conclusion of :math:`a` is equivalent to one of
the premises in :math:`b`.

In taupy, you don't have to input these relations manually. They are determined automatically from the 
arguments in your input. 

How to input arguments and debates in taupy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taupy provides an `Argument` and a `Debate` object. Arguments and debates are input into taupy by
creating new instances of these objects.

But first, we need some sentence variables. Note that this is a major difference to the TDS implementation in Mathematica: Every variable 
needs to be declared before it can be used. For symbolic manipulation and Boolean algebra, `taupy` 
relies on `sympy`, and so we need some `sympy` symbols to input sentence variables: 

.. code:: python

   from taupy import * 
   from sympy import symbols
   # Alternatively: from sympy.abc import a,b,c,...

   a,b,c = symbols("a b c")

Now that we have three sentence variables, we can construct a simple argument with two premises and 
one conclusion:

.. code:: python   

   # An argument with premises a and b, conclusion ~c.
   Argument(a&b,~c)

Note how we have taken the negation of `c` as a premise here by using the `sympy` operator `~`. 
For a debate, we need at least two arguments. Ideally, these two arguments would relate.

.. code:: python  

   # A Debate consisting of two Arguments:
   d,e = symbols("d e")
   tau1 = Debate(Argument(a&b,~c), Argument(~d&e, ~a))

Can you guess, from the description above, whether the two arguments are related in the attack or the 
support manner?

Positions in TDS and their implementation in taupy
--------------------------------------------------
Arguments display relations between propositions, but although arguments are understood to be valid, 
valid arguments can still be rejected. For example, agents can doubt the truth of a premise (or remain
agnostic on the issue). In TDS, the idea that agents can assign truth values to propositions is formulated 
by a position.

The debate `tau1` from the example above has five propositions: a, b, c, d and e. All atomic propositins 
that are part of a debate form the debate's sentence pool. A position in TDS is a mapping from this 
sentence pool to a domain of truth values (in the simplest case, True or False, but this domain can be
extended). To visualise a position :math:`p_1`:

.. math::

   p_1 = \left\{ \begin{array}{l}
                    a \to \text{True}\\
                    b \to \text{False}\\
                    c \to \text{True}\\
                 \end{array} \right\}

A position does not need to assign a truth value to every sentence in the pool. A position that does not, 
as the above example :math:`p`, is called *partial*. A *complete* position assigns a truth value to every
proposition in the debate. 

In `taupy`, positins are a third kind of object: a `Position`. Positions are always relative to a debate,
which should be given as the first argument when creating a new `Position` object. The truth-value assignment
(TVA) is given as a Python dictionary in the second argument:

.. code:: python

   pos1 = Position(tau1, {a: True, b: False, c: True})
   # Check whether it is complete, i.e. assigns True or False to any sentence in its Debate:
   pos1.is_complete()

Positions can be complete or partial, and they have two more important properties: coherence and closedness.

Closedness
   A position is closed if it follows its dialectical obgliations: if a position assigns True to all
   premises in an argument, it must also assign True to the conclusion.

Coherence
   A position is coherent if it fulfils two conditions:

   1. The position assigns identical truth values to equivalent sentences and complementary truth values to incompatible sentences.
   2. The position is closed, i.e. if it accepts all premises of an argument, it also accepts the conclusion.

.. code:: python

   # Check whether the position is coherent:
   pos1.is_coherent()

   # Check whether it follows its "dialectical obligations", i.e. whether it is closed:
   pos1.is_closed()
