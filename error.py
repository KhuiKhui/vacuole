
class Error:
    def __init__ (self, name, details, error_line, error_char, fn):
        self.name = name
        self.details = details
        self.error_line = error_line
        self.error_char = error_char
        self.fn = fn
    def __repr__(self):
        return f"At {self.fn}\nL{self.error_line}-C{self.error_char} {self.name}: {self.details}"
    
class IllegalCharError(Error):
    def __init__(self, details, error_line, error_char, fn):
        super().__init__('Illegal Character', details, error_line, error_char, fn)