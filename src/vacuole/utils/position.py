class Position:
    def __init__(self, fn, line, char):
        self.fn = fn
        self.line = line
        self.char = char
        self.tracking_char = char
    def advance(self, current_char=None, step=1):
        self.char += step
        self.tracking_char += step
        if current_char == "\n":
            self.tracking_char = 0
            self.line += 1
    def copy(self):
        return Position(self.fn, self.line, self.char)