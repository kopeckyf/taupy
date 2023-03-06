Arguments
*********

TDS understands arguments as premise-conclusion structures. This means that any 
argument has a set of premises :math:`\left\{ a_1, a_2, ... a_n \right\}`, a rule 
of inference :math:`r` and a conclusion :math:`c`. :py:mod:`taupy` does not 
implement the rule of inference since it assumes logical validity for any argument. 
Then, the logical structure of an argument is that of an implication: 
:math:`\left\{ a_1, a_2, ... a_n \right\} \to c`.

:py:mod:`taupy` implements arguments as implication relations from :py:mod:`sympy`,
a package for symbolic computing in Python. :py:mod:`taupy` entirely relies on 
:py:mod:`sympy` for symbolic manipulation and some Boolean algebra. In other 
words, the :py:class:`taupy.Argument` class is a sub-class of 
:py:class:`sympy.Implies`.

.. autoclass:: taupy.basic.core.Argument

For the creation of :py:class:`Argument` instances, sentence variables need to 
be present. In the interactive mode, it is recommended to create such objects as
:py:class:`sympy.Symbol` objects via the :py:func:`sympy.symbols` function. 
It is impossible to use sentence variables without declaring them first. This
is due to a core principle in Python: every variable needs to be declared before 
it can be used.

.. code:: python

   from taupy import Argument
   from sympy import symbols
   
   a, b, c = symbols("a b c")
   # Alternatively, but for limited amount of variables only: 
   # from sympy.abc import a, b, c, d, e, ...

Now that we have three sentence variables, we can construct a simple argument 
:py:obj:`a1` with two premises and one conclusion:

.. code:: python   

   a1 = Argument(a&b, ~c)

The premises :py:obj:`a&b` are conntected by the operator `&`, not by
a comma. Premises and conclusion make up two parameters for the instance of an
:py:class:`Argument`, and these are separated by a `,`. We have taken the 
negation of :py:obj:`c` as a premise here by using the :py:mod:`sympy` operator 
`~`. Alternatively, we could have used :py:func:`sympy.Not`. We could have done the same for any of the premises. And we could have 
entered further premises by adding them with a `&`. 
