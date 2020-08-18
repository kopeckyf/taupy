class Position(dict):
    """
    A dictionary that contains sentences 
    """
    def __init__(self, debate, *args):
        self.debate = debate
        dict.__init__(self, *args)
        
    def is_complete(self):
        return True if self.keys() == self.debate.atoms() else False
    
    def is_coherent(self):    
        return True if satisfiable(And(dict_to_prop(self), self.debate)) else False
