from graph_tool.all import Graph, graph_draw, remove_parallel_edges

from taupy.basic import Argument, Debate

# colour          R    G    B    Transparency
attackcolour  = (1.0, 0.0, 0.0, 1.0)
supportcolour = (0.0, 1.0, 0.0, 1.0)

def plot_map(_debate):
    _g = Graph(directed=True)
    
    _names = _g.new_vertex_property("string")
    
    for a in _debate.map().keys():
        _g.add_vertex()
        _names[a] = str(_debate.args[a])
    
    _colours = _g.new_edge_property("vector<double>")
    
    for s in _debate.map().keys():
        for t in _debate.map()[s].keys():
            _currentedge = _g.add_edge(s, t)
            if _debate.map()[s][t]['edge_color'] == 'attack':
                _colours[_currentedge] = attackcolour
            if _debate.map()[s][t]['edge_color'] == 'support':
                _colours[_currentedge] = supportcolour
    
    graph_draw(_g, vertex_text=_names, edge_color = _colours)
        
    
def plot_sccp(_debate):
    
    _g = Graph(directed=False)
    _edgelist = [(_pos1, _pos2) for _pos1 in _debate.sccp().keys() for _pos2 in _debate.sccp()[_pos1]]

    _g.add_edge_list(_edgelist, hashed=True, string_vals=True)
    remove_parallel_edges(_g)
    graph_draw(_g)
