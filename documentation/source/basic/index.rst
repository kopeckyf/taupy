Base objects
************

The theory of dialectical structures is an abstract representation of 
deliberation. It uses three main object types to do so. A :py:class:`Debate` 
is composed of a set of arguments as well as a support and defeat relation 
between them. An :py:class:`Argument` consists of premises and a conclusion.
The relations between arguments are automatically determined through their 
premises and conclusions. An agent's belief system that it forms in light of 
the debate is described as a :py:class:`Position`.

.. toctree::
   
   arguments
   debates
   positions
