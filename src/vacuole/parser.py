from vacuole.nodes import *
from constants.tokens import *
from vacuole.errors import *
from vacuole.utils.position import *

class ParseResult:
    def __init__(self) -> None:
        self.result = None
        self.error = None
    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.result
        return res
    def success(self, res):
        self.result = res
        return self
    def failure(self, error):
        self.error = error
        return self


class Parser:

    def __init__(self, fn, tokens) -> None:
        self.fn = fn
        self.tokens = tokens
        self.pos = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else self.current_token
    
    def bin_op(self, func, ops):
        parseRes = ParseResult()
        left = parseRes.register(func())
        if parseRes.error: return parseRes
        
        while self.current_token.type in ops:
            op = self.current_token.type
            self.advance()
            right = parseRes.register(func())
            if parseRes.error: return parseRes
            left = parseRes.success(BinOpNode(left, op, right))
        return left

    def expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))
    
    def factor(self):
        parseRes = ParseResult()
        token = self.current_token
        if token.type in (TT_PLUS, TT_MINUS):
            self.advance()
            factor = parseRes.register(self.factor())
            if parseRes.error: return parseRes
            return parseRes.register(UnaryOpNode(token, factor))
        if token.type == TT_LPAREN:
            self.advance()
            expr = parseRes.register(self.expr())
            if parseRes.error: return parseRes
            if self.current_token.type == TT_RPAREN:
                self.advance()
                return parseRes.success(expr)
            else:
                return parseRes.failure(InvalidSyntaxError("')' expected.", self.current_token.line, self.current_token.end, self.fn))

        if token.type in (TT_INT, TT_FLOAT):
            self.advance()
            return parseRes.success(NumberNode(token))
        return parseRes.failure(IllegalCharError("Must be type integer or float.", self.current_token.line, self.current_token.end, self.fn))
        
    def parse(self):
        parseRes = ParseResult()
        res = parseRes.register(self.expr())
        error = parseRes.error
        if not error and self.current_token.type != TT_EOF:
            error = InvalidSyntaxError("Expression with missing terms found.", self.current_token.line, self.current_token.end, self.fn)

        return res, error
