from vacuole.nodes import *
from constants.tokens import *
from constants.text import *
from vacuole.errors import *
from vacuole.lexer import *
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
        self.pos = 0
        self.current_token = self.tokens[self.pos]
        self.indent_level = 0

    def advance(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else self.current_token

    def parse(self):
        parseRes = ParseResult()
        res = parseRes.register(self.program())
        error = parseRes.error
        if not error and self.current_token.type != TT_EOF:
            error = InvalidSyntaxError("Expression with missing terms found.", self.current_token.pos)

        return res, error
    
    def program(self):
        parseRes = ParseResult()
        program_node = ProgramNode()
        while self.pos < len(self.tokens) and self.current_token.type != TT_EOF:
            if self.current_token.type == TT_NEWLINE:
                self.advance()
                
            node = parseRes.register(self.expr())
            program_node.addNode(node)
            #print(self.current_token)
            
        return program_node

    def expr(self):
        parseRes = ParseResult()
        if self.current_token.value in TYPES:
            return self.var_assign()
        elif self.current_token.type == TT_IDENTIFIER:
            return self.var_update()
        elif self.current_token.matches(TT_KEYWORD, ["if", "else if", "else"]):
            return self.if_else_block()
        return self.cond_expr()
    
    def if_else_block(self):
        if_block = None
        if self.current_token.matches(TT_KEYWORD, "if"):
            if_block = self.if_expr()
        
        if if_block != None:
            if self.current_token.matches(TT_KEYWORD, "else if"):
                else_if_block = self.if_expr()

                if_block.addCase(else_if_block.cases[0]["condition"], else_if_block.cases[0]["action"])
            if self.current_token.matches(TT_KEYWORD, "else"):
                else_block = self.else_expr()
                if_block.addCase(else_block.cases[0]["condition"], else_block.cases[0]["action"])
        return if_block

    def else_expr(self):
        parseRes = ParseResult()
        if_program_node = ProgramNode()
        self.advance()

        parseRes.register(self.is_syntax_correct())
        if parseRes.error: return parseRes

        action_node = parseRes.register(self.expr())
        if parseRes.error: return parseRes
        if_program_node.addNode(action_node)

        if_program_node = parseRes.register(self.get_subsequent_actions(if_program_node))
        if parseRes.error: return parseRes
            
        return parseRes.register(IfNode(self.indent_level).addCase(NumberNode(Token(TT_INT, 1, self.current_token.pos), self.indent_level), if_program_node))

    def if_expr(self):
        parseRes = ParseResult()
        if_program_node = ProgramNode()
        self.advance()

        if_condition_node = parseRes.register(self.get_condition())
        if parseRes.error: return parseRes

        parseRes.register(self.is_syntax_correct())
        if parseRes.error: return parseRes

        action_node = parseRes.register(self.expr())
        if parseRes.error: return parseRes
        if_program_node.addNode(action_node)

        if_program_node = parseRes.register(self.get_subsequent_actions(if_program_node))
        if parseRes.error: return parseRes
       
            
        return parseRes.register(IfNode(self.indent_level).addCase(if_condition_node, if_program_node))

    def get_condition(self):
        parseRes = ParseResult()
        if_condition_node = parseRes.register(self.expr())
        if parseRes.error: return parseRes
        return parseRes.success(if_condition_node)
    
    def is_syntax_correct(self):
        parseRes = ParseResult()
        if self.current_token.type != TT_COLON:
            return parseRes.failure(InvalidSyntaxError("Missing ':'.", self.current_token.pos))
        self.advance()
        
        while self.current_token.type == TT_NEWLINE:
            self.advance()
        if self.current_token.type != TT_INDENT:
            return parseRes.failure(IndentationError("Found lower level of indentation.", self.current_token.pos))
        self.advance()
        if self.current_token.type == TT_INDENT:
            return parseRes.failure(IndentationError("Found higher level of indentation.", self.current_token.pos))
        return parseRes
    
    def get_subsequent_actions(self, nodes):
        parseRes = ParseResult()
        
        while True:
            while self.current_token.type == TT_NEWLINE:
                self.advance()
            if self.current_token.type != TT_INDENT:
                break
            self.advance()
            if self.current_token.type == TT_INDENT:
                return parseRes.failure(IndentationError("Found higher level of indentation.", self.current_token.pos))
            action_node = parseRes.register(self.expr())
            if parseRes.error: return parseRes
            nodes.addNode(action_node)

        return parseRes.success(nodes)
        
    def cond_expr(self):
        return self.bin_op(self.comp_expr, (TT_AND, TT_OR, TT_BIT_AND, TT_BIT_OR))
        
    def bin_op(self, func, ops):
        parseRes = ParseResult()
        left = parseRes.register(func())
        if parseRes.error: return parseRes
        while self.current_token.type in ops:
            left = parseRes.register(left)
            op = self.current_token
            self.advance()
            right = parseRes.register(func())
            if parseRes.error: return parseRes
            left = parseRes.success(BinOpNode(left, op, right, self.indent_level))

        return left

    def comp_expr(self):
        parseRes = ParseResult()
        if self.current_token.type == TT_NOT:
            op_token = self.current_token
            self.advance()
            node = parseRes.register(self.comp_expr())
            return UnaryOpNode(op_token, node, self.indent_level)
        node = parseRes.register(self.bin_op(self.arith_expr, COMP_OPS))
        if parseRes.error: return parseRes
        return node
    
    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS, TT_POWER))

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV, TT_MOD, TT_POWER))
    
    def factor(self):
        parseRes = ParseResult()
        token = self.current_token
        if token.type == TT_INDENT:
            self.indent_level += 1
        if token.type == TT_IDENTIFIER:
            token_identifier = self.current_token
            self.advance()
            return self.var_access(token_identifier)
        if token.type in (TT_PLUS, TT_MINUS): 
            self.advance()
            factor = parseRes.register(self.factor())
            if parseRes.error: return parseRes
            return parseRes.register(UnaryOpNode(token, factor, self.indent_level))
        if token.type == TT_LPAREN:
            self.advance()
            expr = parseRes.register(self.expr())
            if parseRes.error: return parseRes
            if self.current_token.type == TT_RPAREN:
                self.advance()
                return parseRes.success(expr)
            else:
                return parseRes.failure(InvalidSyntaxError("')' expected.", self.current_token.pos))

        if token.type in (TT_INT, TT_FLOAT):
            self.advance()
            return parseRes.success(NumberNode(token, self.indent_level))
        
        if self.current_token.type == TT_EOF:
            return parseRes.failure(InvalidSyntaxError(f"Expression with missing terms found.", self.current_token.pos))

        return parseRes.failure(InvalidSyntaxError(f"Must be type integer or float, not '{self.current_token.value}'", self.current_token.pos))

    def var_update(self):
        parseRes = ParseResult()
        
        identifier_token = self.current_token
        
        if self.pos < len(self.tokens) - 1:
            if self.tokens[self.pos + 1].type == TT_EQ:
                self.advance()
                self.advance()
                expr = parseRes.register(self.expr())
                if parseRes.error: return parseRes
                return parseRes.success(VarUpdateNode(identifier_token, expr, self.indent_level))
            
        return self.bin_op(self.comp_expr, (TT_AND, TT_OR, TT_BIT_AND, TT_BIT_OR))

    def var_assign(self):
        parseRes = ParseResult()
        keyword = self.current_token.value
        self.advance()
        parseRes.register(self.current_token)
        if self.current_token.type != TT_IDENTIFIER:
            return parseRes.failure(InvalidSyntaxError("Identifier expected.", self.current_token.pos))
        if self.current_token.value in CONSTANTS:
            return parseRes.failure(IllegalCharError("Keyword used as identifier.", self.current_token.pos))
        identifier_token = self.current_token
        self.advance()
        if self.current_token.type != TT_EQ:
            return parseRes.failure(InvalidSyntaxError("'=' expected.", self.current_token.pos))
        self.advance()
        expr = parseRes.register(self.expr())
        if parseRes.error: return parseRes
        return parseRes.success(VarAssignNode(keyword, identifier_token, expr, self.indent_level))
    
    def var_access(self, identifier_token):
        parseRes = ParseResult()
        return parseRes.success(VarAccessNode(identifier_token, self.indent_level))
    
    
    