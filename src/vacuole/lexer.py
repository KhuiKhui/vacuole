from vacuole.errors import *
from constants.tokens import *
from constants.text import *
from vacuole.utils.position import *
    

class Token:
    def __init__ (self, type, value, pos) -> None:
        self.type = type
        self.value = value
        self.pos = pos
        
    def __repr__(self) -> str:
        return f"{self.type}:{self.value}"


class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(fn, 1, 0)
        self.current_char = self.text[0]
        
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
            return Token(TT_INT, int(number), self.pos)
        else:
            return Token(TT_FLOAT, float(number), self.pos)


    def tokenize(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in " \t":
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.processDigits())
            elif self.current_char == "+":
                tokens.append(Token(TT_PLUS, "+", self.pos))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Token(TT_MINUS, "-", self.pos))
                self.advance()
            elif self.current_char == "*":
                if self.pos.char < len(self.text)-1:
                    if self.text[self.pos.char + 1] == "*":
                        tokens.append(Token(TT_POWER, "**", self.pos))
                        self.advance()
                        self.advance()
                        continue
                tokens.append(Token(TT_MUL, "*", self.pos))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(TT_DIV, "/", self.pos))
                self.advance()

            elif self.current_char == "(":
                tokens.append(Token(TT_LPAREN, "(", self.pos))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(TT_RPAREN, ")", self.pos))
                self.advance()
            else:
                error_char = self.current_char
                self.advance()
                return [], IllegalCharError(error_char, self.pos)
        tokens.append(Token(TT_EOF, "EOF", self.pos))
        return tokens, None
        
