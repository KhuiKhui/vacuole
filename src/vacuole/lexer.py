from vacuole.errors import *
from constants.tokens import *
from constants.text import *
from vacuole.utils.position import *
    

class Token:
    def __init__ (self, type, value, line, start, end) -> None:
        self.type = type
        self.value = value
        self.start = start
        self.end = start + 1
        self.line = line
        if end:
            self.end = end
        
    def __repr__(self) -> str:
        return f"{self.type}:{self.value}"


class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 1, fn)
        self.current_char = ""
        self.advance()
        
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.char] if self.pos.char < len(self.text) else None

    def processDigits(self):
        number = ""
        dot_count = 0
        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                dot_count += 1
                number += "."
            else:
                number += self.current_char
            self.advance()
        
        if dot_count == 0:
            return Token(TT_INT, int(number), self.pos.line, self.pos.char-len(number), self.pos.char)
        else:
            return Token(TT_FLOAT, float(number), self.pos.line, self.pos.char-len(number), self.pos.char)


    def tokenize(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in " \t":
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.processDigits())
            elif self.current_char == "+":
                tokens.append(Token(TT_PLUS, "+", self.pos.line, self.pos.char-len(self.current_char), self.pos.char))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Token(TT_MINUS, "-", self.pos.line, self.pos.char-len(self.current_char), self.pos.char))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(TT_MUL, "*", self.pos.line, self.pos.char-len(self.current_char), self.pos.char))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(TT_DIV, "/", self.pos.line, self.pos.char-len(self.current_char), self.pos.char))
                self.advance()
            # elif self.current_char + self.text[self.pos + 1] == "**":
            #     tokens.append(Token(TT_POWER, "**", self.pos.line, self.pos.char-len(self.current_char), self.pos.char))
            #     self.advance()
            elif self.current_char == "(":
                tokens.append(Token(TT_LPAREN, "(", self.pos.line, self.pos.char-len(self.current_char), self.pos.char))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(TT_RPAREN, ")", self.pos.line, self.pos.char-len(self.current_char), self.pos.char))
                self.advance()
            else:
                error_char = self.current_char
                self.advance()
                return [], IllegalCharError(error_char, self.pos.line, self.pos.char, self.fn)
        tokens.append(Token(TT_EOF, "EOF", self.pos.line, self.pos.char, self.pos.char))
        return tokens, None
        
