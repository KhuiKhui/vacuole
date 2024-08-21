
class Error:
    def __init__ (self, name, details, pos):
        self.name = name
        self.details = details
        self.pos = pos
    def __repr__(self):
        return f"At {self.pos.fn}\nL{self.pos.line}-C{self.pos.char} {self.name}: {self.details}"
    
class IllegalCharError(Error):
    def __init__(self, details, pos):
        super().__init__('Illegal Character', details, pos)

class InvalidSyntaxError(Error):
    def __init__(self, details, pos):
        super().__init__('Invalid Syntax', details, pos)

class RuntimeError(Error):
    def __init__(self, details, pos):
        super().__init__('Runtime Error', details, pos)