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
        self.text = self.clean_input(text)
        self.pos = Position(fn, line_number, 0)
        self.current_char = self.text[0]
        self.tokens = []

    def clean_input(self, text):
        return text.strip("\n")
        
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.char] if self.pos.char < len(self.text) else None
    
    def process_indent(self):
        spaces_until_tab = 0
        while self.current_char == " ":
            spaces_until_tab += 1
            
            if spaces_until_tab == 4:
                return Token(TT_INDENT, "\\t", self.pos)
            self.advance()
        return None

    def process_digits(self):
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

    def process_text(self):
        text = ""
        while self.current_char != None and self.current_char in DIGITS_AND_LETTERS + "_":
            text += self.current_char
            self.advance()
        return text
    
    def process_variable(self):
        id_str = self.process_text()
        token_type = TT_KEYWORD if id_str in TYPES + FUNCTIONS else TT_IDENTIFIER
        return Token(token_type, id_str, self.pos)
    
    def process_string(self):
        string = self.process_text()
        return Token(TT_STRING, string, self.pos)
    
    def process_quotes(self, starting_quotes=None):
        cur_quotes = self.current_char
        if starting_quotes != None and starting_quotes != cur_quotes:
            return [], IllegalCharError(f"Illegal quote placement: {cur_quotes}", self.pos)
        quotes_type = TT_DOUBLE_QUOTES if cur_quotes == '"' else TT_SINGLE_QUOTES
        pos = self.pos
        self.advance()
        return Token(quotes_type, cur_quotes, pos), None
    
    def perform_token_merges(self):
        self.merge_else_if_tokens()

    def merge_else_if_tokens(self):
        if len(self.tokens) < 2:
            return
        if self.tokens[-2].matches(TT_KEYWORD, "else") and self.tokens[-1].matches(TT_KEYWORD, "if"):
            self.tokens.pop(-1)
            self.tokens.pop(-1)
            self.tokens.append(Token(TT_KEYWORD, "else if", self.pos))

    def add_token(self, token_type, token_value, full_token_type=None, second_token_value=None):
        
        if self.pos.char < len(self.text)-1 and full_token_type != None and second_token_value != None:
            if self.text[self.pos.char + 1] == second_token_value:
                self.tokens.append(Token(full_token_type, token_value + second_token_value, self.pos))
                self.advance()
                self.advance()
                return
                
        self.tokens.append(Token(token_type, token_type, self.pos))
        self.advance()

    def tokenize(self):
        while self.current_char != None:        
            if self.current_char == " " and (len(self.tokens) == 0 or self.tokens[-1].type in (TT_NEWLINE, TT_INDENT)):
                indent_token = self.process_indent()
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
                opening_quotes, opening_error = self.process_quotes()
                string_token = self.process_string()
                ending_quotes, ending_error = self.process_quotes(opening_quotes.value)
                if ending_error != None:
                    return [], ending_error
                self.tokens.append(opening_quotes)
                self.tokens.append(string_token)
                self.tokens.append(ending_quotes)

            elif self.current_char in DIGITS:
                self.tokens.append(self.process_digits())

            elif self.current_char in LETTERS + "_":
                self.tokens.append(self.process_variable())
                self.perform_token_merges()
            
            elif self.current_char == ">":
                self.add_token(TT_GREATER_THAN, ">", TT_GREATER_OR_EQ_TO, "=")
            elif self.current_char == "<":
                self.add_token(TT_LESS_THAN, "<", TT_LESS_OR_EQ_TO, "=")
            elif self.current_char == "+":
                self.add_token(TT_PLUS, "+")
            elif self.current_char == "-":
                self.add_token(TT_MINUS, "-")
            elif self.current_char == "*":
                self.add_token(TT_MUL, "*", TT_POWER, "*")
            elif self.current_char == "/":
                self.add_token(TT_DIV, "/", TT_REMAINDER, "/")
            elif self.current_char == "%":
                self.add_token(TT_MOD, "%")
            elif self.current_char == "(":
                self.add_token(TT_LPAREN, "(")
            elif self.current_char == ")":
                self.add_token(TT_RPAREN, ")")
            elif self.current_char == "=":
                self.add_token(TT_EQ, "=", TT_EQ_TO, "=")
            elif self.current_char == "!":
                self.add_token(TT_NOT, "!", TT_NOT_EQ_TO, "=")
            elif self.current_char == "&":
                self.add_token(TT_BIT_AND, "&", TT_AND, "&")
            elif self.current_char == "|":
                self.add_token(TT_BIT_OR, "|", TT_OR, "|")
            elif self.current_char == "^":
                self.add_token(TT_BIT_XOR, "^")
            elif self.current_char == "~":
                self.add_token(TT_BIT_NOT, "~")
            elif self.current_char == ":":
                self.add_token(TT_COLON, ":")
            elif self.current_char == ";":
                self.add_token(TT_SEMI_COLON, ";")
            else:
                error_char = self.current_char
                self.advance()
                return [], IllegalCharError(error_char, self.pos)
        self.tokens.append(Token(TT_EOF, "EOF", self.pos))
        return self.tokens, None
        
