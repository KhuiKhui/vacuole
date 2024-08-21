class Boolean:
    def __init__(self, expr):
        self.expr = expr
        self.set_pos()
    def set_pos(self, start=None, end=None):
        self.start = start
        self.end = end
    def add_to(self, other):
        if isinstance(other, Boolean):
            return Boolean(self.expr == other.expr)
    
    def __repr__(self) -> str:
        return str(self.Boolean)