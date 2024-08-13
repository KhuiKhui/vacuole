from error import *

TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
DIGITS = "0123456789"

class Position:
    def __init__(self, char, line, fn):
        self.char = char
        self.line = line
        self.fn = fn
    def advance(self, current_char):
        self.char += 1
        if current_char == "\n":
            self.char = 0
            self.line += 1
    

class Token:
    def __init__ (self, type, value=None) -> None:
        self.type = type
        self.value = value
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
            return Token(TT_INT, int(number))
        else:
            return Token(TT_FLOAT, float(number))


    def tokenize(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in " \t":
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.processDigits())
            elif self.current_char == "+":
                tokens.append(Token(TT_PLUS, "+"))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Token(TT_MINUS, "-"))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(TT_MUL, "*"))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(TT_DIV, "/"))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(TT_LPAREN, "("))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(TT_RPAREN, ")"))
                self.advance()
            else:
                error_char = self.current_char
                self.advance()
                return [], IllegalCharError(error_char, self.pos.line, self.pos.char, self.fn)

        return tokens, None
        
