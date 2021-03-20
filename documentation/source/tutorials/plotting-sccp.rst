Tutorial A: Plotting the SCCP
*****************************

In this tutorial, we will be using the drawing capabilities 
from :py:obj:`networkx` to plot a simple debate's space of
coherent and complete positions (SCCP).

Let's go ahead with a really simple debate:

.. code:: python

    from taupy import * 
    from sympy import symbols
    
    # declare five sentence variables
    p1, p2, p3, p4, p5 = symbols("p:5")

    # create a simple debate with two arguments.
    d = Debate(Argument(p1&p2&p3, p4), Argument(p5&~p2, ~p4))
    
:py:meth:`taupy.basic.core.Base.sccp` returns a dictionary of list representation of a graph,
which can be easily imported by :py:obj:`networkx`.

.. code:: python

    import networkx as nx
    
    # create the graph with the sccp() method of the Debate object.
    graph = nx.from_dict_of_lists(d.sccp())
    
    # choose a layout (optional)
    layout = nx.kamada_kawai_layout(graph)
    
    # plot the graph. networkx uses matplotlib here.
    nx.draw(graph, pos=layout, with_labels=True, node_color="#aaa")

And this returns the figure below. In the figure, nodes have a label that shows
the bit string representation of the position they resemble. In this bit string,
propositions are ordered alphabetically (`p1` will show in the first bit, `p5`
in the last), and they are either `0` if the position assigns False to this 
proposition, or `1` if the position accepts the proposition. Positions are 
connected by an edge if they differ in exactly one truth-value attribution (i.e.,
if their Hamming distance equals 1).

.. image:: tutorials_example_sccp.png
