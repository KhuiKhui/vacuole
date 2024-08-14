class Position:
    def __init__(self, char, line, fn):
        self.char = char
        self.line = line
        self.fn = fn
    def advance(self, current_char=None, step=1):
        self.char += step
        if current_char == "\n":
            self.char = 0
            self.line += 1