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
        self.tokens = []
        
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.char] if self.pos.char < len(self.text) else None
    
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
        

    def processText(self):
        text = ""
        
        while self.current_char != None and self.current_char in DIGITS_AND_LETTERS + "_":
            
            
            text += self.current_char
            
            self.advance()
        return text
    
    def processVariable(self):
        id_str = self.processText()
        
        token_type = TT_KEYWORD if id_str in TYPES + FUNCTIONS else TT_IDENTIFIER
        return Token(token_type, id_str, self.pos)
    
    def processString(self):
        string = self.processText()
        
        return Token(TT_STRING, string, self.pos)
    
    def processQuotes(self, starting_quotes=None):
        cur_quotes = self.current_char

        if starting_quotes != None and starting_quotes != cur_quotes:
            return [], IllegalCharError(f"Illegal quote placement: {cur_quotes}", self.pos)
        
        quotes_type = TT_DOUBLE_QUOTES if cur_quotes == '"' else TT_SINGLE_QUOTES
        pos = self.pos
        self.advance()
        
        return Token(quotes_type, cur_quotes, pos), None
    
    
    def mergeElseIfTokens(self):
        if len(self.tokens) < 2:
            return
        if self.tokens[-2].matches(TT_KEYWORD, "else") and self.tokens[-1].matches(TT_KEYWORD, "if"):
            self.tokens.pop(-1)
            self.tokens.pop(-1)
            self.tokens.append(Token(TT_KEYWORD, "else if", self.pos))


    def tokenize(self):
        
        while self.current_char != None:
            #print(f"'{self.current_char}'")
            
            if self.current_char == " " and (len(self.tokens) == 0 or self.tokens[-1].type in (TT_NEWLINE, TT_INDENT)):
                indent_token = self.processIndent()
                
                if indent_token == None: return [], IndentationError("Vacuole only supports tab indentation.", self.pos)
                self.advance()
                self.tokens.append(indent_token)
            elif self.current_char == "\n":
                if len(self.tokens) == 0 or self.tokens[-1].type in (TT_NEWLINE, TT_INDENT):
                    self.advance()
                else:
                    self.tokens.append(Token(TT_NEWLINE, "\\n", self.pos))
                    self.advance()
            elif self.current_char == " ":
                self.advance()
            elif self.current_char == "\"" or self.current_char == "'":
                opening_quotes, opening_error = self.processQuotes()
                string_token = self.processString()
                ending_quotes, ending_error = self.processQuotes(opening_quotes.value)
                if ending_error != None:
                    return [], ending_error
                
                self.tokens.append(opening_quotes)
                self.tokens.append(string_token)
                self.tokens.append(ending_quotes)

            elif self.current_char in DIGITS:
                self.tokens.append(self.processDigits())
            elif self.current_char in LETTERS + "_":
                self.tokens.append(self.processVariable())
                self.mergeElseIfTokens()
            
                
            elif self.current_char == ">":
                if self.pos.char < len(self.text)-1:
                    if self.text[self.pos.char + 1] == "=":
                        self.tokens.append(Token(TT_GREATER_OR_EQ_TO, ">=", self.pos))
                        self.advance()
                        self.advance()
                        continue
                self.tokens.append(Token(TT_GREATER_THAN, ">", self.pos))
                self.advance()
            elif self.current_char == "<":
                if self.pos.char < len(self.text)-1:
                    if self.text[self.pos.char + 1] == "=":
                        self.tokens.append(Token(TT_LESS_OR_EQ_TO, "<=", self.pos))
                        self.advance()
                        self.advance()
                        continue
                self.tokens.append(Token(TT_LESS_THAN, "<", self.pos))
                self.advance()
            elif self.current_char == "+":
                self.tokens.append(Token(TT_PLUS, "+", self.pos))
                self.advance()
            elif self.current_char == "-":
                self.tokens.append(Token(TT_MINUS, "-", self.pos))
                self.advance()
            elif self.current_char == "*":
                if self.pos.char < len(self.text)-1:
                    if self.text[self.pos.char + 1] == "*":
                        self.tokens.append(Token(TT_POWER, "**", self.pos))
                        self.advance()
                        self.advance()
                        continue
                self.tokens.append(Token(TT_MUL, "*", self.pos))
                self.advance()
            elif self.current_char == "/":
                self.tokens.append(Token(TT_DIV, "/", self.pos))
                self.advance()
            elif self.current_char == "%":
                self.tokens.append(Token(TT_MOD, "%", self.pos))
                self.advance()
            elif self.current_char == "(":
                self.tokens.append(Token(TT_LPAREN, "(", self.pos))
                self.advance()
            elif self.current_char == ")":
                self.tokens.append(Token(TT_RPAREN, ")", self.pos))
                self.advance()
            elif self.current_char == "=":
                if self.pos.char < len(self.text)-1:
                    if self.text[self.pos.char + 1] == "=":
                        self.tokens.append(Token(TT_EQ_TO, "==", self.pos))
                        self.advance()
                        self.advance()
                        continue
                self.tokens.append(Token(TT_EQ, "=", self.pos))
                self.advance()
            elif self.current_char == "!":
                if self.pos.char < len(self.text)-1:
                    if self.text[self.pos.char + 1] == "=":
                        self.tokens.append(Token(TT_NOT_EQ_TO, "!=", self.pos))
                        self.advance()
                        self.advance()
                        continue
                self.tokens.append(Token(TT_NOT, "!", self.pos))
                self.advance()
            elif self.current_char == "&":
                if self.pos.char < len(self.text)-1:
                    if self.text[self.pos.char + 1] == "&":
                        self.tokens.append(Token(TT_AND, "&&", self.pos))
                        self.advance()
                        self.advance()
                        continue
                self.tokens.append(Token(TT_BIT_AND, "&", self.pos))
                self.advance()
            elif self.current_char == "|":
                if self.pos.char < len(self.text)-1:
                    if self.text[self.pos.char + 1] == "|":
                        self.tokens.append(Token(TT_OR, "||", self.pos))
                        self.advance()
                        self.advance()
                        continue
                self.tokens.append(Token(TT_BIT_OR, "|", self.pos))
                self.advance()
            elif self.current_char == "^":
                self.tokens.append(Token(TT_BIT_XOR, "^", self.pos))
                self.advance()
            elif self.current_char == "~":
                self.tokens.append(Token(TT_BIT_NOT, "~", self.pos))
                self.advance()
            elif self.current_char == ":":
                self.tokens.append(Token(TT_COLON, ":", self.pos))
                self.advance()
            elif self.current_char == ";":
                self.tokens.append(Token(TT_SEMI_COLON, ";", self.pos))
                self.advance()
            else:
                error_char = self.current_char
                self.advance()
                return [], IllegalCharError(error_char, self.pos)
        self.tokens.append(Token(TT_EOF, "EOF", self.pos))
        return self.tokens, None
        
