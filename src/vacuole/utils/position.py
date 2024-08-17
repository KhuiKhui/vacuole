class Position:
    def __init__(self, fn, line, char):
        self.fn = fn
        self.line = line
        self.char = char
    def advance(self, current_char=None, step=1):
        self.char += step
        if current_char == "\n":
            self.char = 0
            self.line += 1