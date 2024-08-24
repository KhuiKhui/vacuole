from vacuole.errors import *
from constants.tokens import *
from constants.text import *
from vacuole.utils.position import *
    

class Token:
    def __init__ (self, type, value, pos) -> None:
        self.type = type
        self.value = value
        self.pos = pos.copy()
        
    def __repr__(self) -> str:
        return f"{self.type}:{self.value}"
    
    def matches(self, type, values):
        return self.type == type and self.value in values

class Lexer:
    def __init__(self, fn, text, line_number):
        self.fn = fn
        self.text = text
        self.pos = Position(fn, line_number, 0)
        self.current_char = self.text[0]
        
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.char] if self.pos.char < len(self.text) else None
        #print(self.current_char)
    
    def processIndent(self):
        spaces_until_tab = 0
        while self.current_char == " ":
            spaces_until_tab += 1
            
            if spaces_until_tab == 4:
                return Token(TT_INDENT, "\\t", self.pos)
            self.advance()
        return None

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
        
    def processVariables(self):
        id_str = ""
        while self.current_char != None and self.current_char in DIGITS_AND_LETTERS + "_":
            #print("LOOP")
            id_str += self.current_char
            self.advance()
        
        token_type = TT_KEYWORD if id_str in TYPES + FUNCTIONS else TT_IDENTIFIER
        return Token(token_type, id_str, self.pos)


    def tokenize(self):
        tokens = []
        while self.current_char != None:
            print(f"'{self.current_char}'")
            
            if self.current_char == " " and (len(tokens) == 0 or tokens[-1].type in (TT_NEWLINE, TT_INDENT)):
                indent_token = self.processIndent()
                
                if indent_token == None: return [], IndentationError("Vacuole only supports tab indentation.", self.pos)
                self.advance()
                tokens.append(indent_token)
            elif self.current_char == "\n":
                tokens.append(Token(TT_NEWLINE, "\\n", self.pos))
                self.advance()
                print(f"AFTER NEWLINE: '{self.current_char}'")
            elif self.current_char == " ":
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.processDigits())
            elif self.current_char in LETTERS + "_":
                tokens.append(self.processVariables())
                
            elif self.current_char == ">":
                if self.pos.char < len(self.text)-1:
                    if self.text[self.pos.char + 1] == "=":
                        tokens.append(Token(TT_GREATER_OR_EQ_TO, ">=", self.pos))
                        self.advance()
                        self.advance()
                        continue
                tokens.append(Token(TT_GREATER_THAN, ">", self.pos))
                self.advance()
            elif self.current_char == "<":
                if self.pos.char < len(self.text)-1:
                    if self.text[self.pos.char + 1] == "=":
                        tokens.append(Token(TT_LESS_OR_EQ_TO, "<=", self.pos))
                        self.advance()
                        self.advance()
                        continue
                tokens.append(Token(TT_LESS_THAN, "<", self.pos))
                self.advance()
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
            elif self.current_char == "%":
                tokens.append(Token(TT_MOD, "%", self.pos))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(TT_LPAREN, "(", self.pos))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(TT_RPAREN, ")", self.pos))
                self.advance()
            elif self.current_char == "=":
                if self.pos.char < len(self.text)-1:
                    if self.text[self.pos.char + 1] == "=":
                        tokens.append(Token(TT_EQ_TO, "==", self.pos))
                        self.advance()
                        self.advance()
                        continue
                tokens.append(Token(TT_EQ, "=", self.pos))
                self.advance()
            elif self.current_char == "!":
                if self.pos.char < len(self.text)-1:
                    if self.text[self.pos.char + 1] == "=":
                        tokens.append(Token(TT_NOT_EQ_TO, "!=", self.pos))
                        self.advance()
                        self.advance()
                        continue
                tokens.append(Token(TT_NOT, "!", self.pos))
                self.advance()
            elif self.current_char == "&":
                if self.pos.char < len(self.text)-1:
                    if self.text[self.pos.char + 1] == "&":
                        tokens.append(Token(TT_AND, "&&", self.pos))
                        self.advance()
                        self.advance()
                        continue
                tokens.append(Token(TT_BIT_AND, "&", self.pos))
                self.advance()
            elif self.current_char == "|":
                if self.pos.char < len(self.text)-1:
                    if self.text[self.pos.char + 1] == "|":
                        tokens.append(Token(TT_OR, "||", self.pos))
                        self.advance()
                        self.advance()
                        continue
                tokens.append(Token(TT_BIT_OR, "|", self.pos))
                self.advance()
            elif self.current_char == ":":
                tokens.append(Token(TT_COLON, ":", self.pos))
                self.advance()
            elif self.current_char == ";":
                tokens.append(Token(TT_SEMI_COLON, ";", self.pos))
                self.advance()
            else:
                error_char = self.current_char
                self.advance()
                return [], IllegalCharError(error_char, self.pos)
        tokens.append(Token(TT_EOF, "EOF", self.pos))
        return tokens, None
        
