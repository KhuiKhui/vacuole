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
        self.tokens = self.clean_tokens(tokens)
        self.pos = 0
        self.current_token = self.tokens[self.pos]
        self.indent_level = 0

    def clean_tokens(self, dirty_tokens):
        new_tokens = []
        if dirty_tokens[0] != "\n":
            new_tokens.append(dirty_tokens[0])
        for i in range(1, len(dirty_tokens)):
            if dirty_tokens[i-1].type == TT_NEWLINE and dirty_tokens[i].type == TT_NEWLINE:
                continue

            if dirty_tokens[i-1].type == TT_INDENT and dirty_tokens[i].type == TT_NEWLINE:
                continue
                
            new_tokens.append(dirty_tokens[i])
        return new_tokens
    
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
        return program_node

            
    def expr(self):
        parseRes = ParseResult()
        self.indent_level = 0
        if self.current_token.value in TYPES:
            return self.var_assign()
        elif self.current_token.type == TT_IDENTIFIER:
            return self.var_update()
        elif self.current_token.matches(TT_KEYWORD, ["if", "else if", "else"]):
            return self.if_else_block()
        elif self.current_token.matches(TT_KEYWORD, "for"):
            return self.for_expr()
            
        return self.cond_expr()
    
    def if_else_block(self):
        if_block = None
        if self.current_token.matches(TT_KEYWORD, "if"):
            if_block = self.if_expr()
        if if_block != None:
            if self.current_token.matches(TT_KEYWORD, "else if"):
                self.advance()
                else_if_block = self.if_expr()

                if_block.add_body(else_if_block.cases[0]["condition"], else_if_block.cases[0]["body"])
            if self.current_token.matches(TT_KEYWORD, "else"):
                self.advance()
                else_block = self.else_expr()
                if_block.add_body(else_block.cases[0]["condition"], else_block.cases[0]["body"])
        return if_block

    def else_expr(self):
        parseRes = ParseResult()
        if_program_node = ProgramNode()
        self.advance()

        parseRes.register(self.is_syntax_correct())
        if parseRes.error: return parseRes

        indent = self.indent_level
        if_program_node = parseRes.register(self.get_bodies(indent))
        if parseRes.error: return parseRes
            
        return parseRes.register(IfNode(self.indent_level).add_body(NumberNode(Token(TT_INT, 1, self.current_token.pos), self.indent_level), if_program_node.nodes))

    def if_expr(self):
        parseRes = ParseResult()
        
        self.advance()

        if_condition_node = parseRes.register(self.get_condition())
        if parseRes.error: return parseRes

        parseRes.register(self.is_syntax_correct())
        if parseRes.error: return parseRes


        indent = self.indent_level
        if_program_node = parseRes.register(self.get_bodies(indent))
        if parseRes.error: return parseRes
            
        return parseRes.register(IfNode(self.indent_level).add_body(if_condition_node, if_program_node.nodes))

    def get_condition(self):
        parseRes = ParseResult()
        if_condition_node = parseRes.register(self.expr())
        if parseRes.error: return parseRes
        return parseRes.success(if_condition_node)
    
    def for_expr(self):
        parseRes = ParseResult()
        self.advance()
        if self.current_token.type == TT_LPAREN:
            self.advance()
            iterator = parseRes.register(self.expr())

            parseRes.register(self.is_separator_correct())
            if parseRes.error: return parseRes

            condition = parseRes.register(self.expr())
            parseRes.register(self.is_separator_correct())
            if parseRes.error: return parseRes
            
            step = parseRes.register(self.expr())
            if parseRes.error: return parseRes

            if self.current_token.type == TT_RPAREN:

                self.advance()
                parseRes.register(self.is_syntax_correct())
                if parseRes.error: return parseRes

                indent = self.indent_level        
                print(indent, self.current_token)
                body_program_node = parseRes.register(self.get_bodies(indent))
                if parseRes.error: return parseRes
                print("BODY: ", body_program_node)
                return parseRes.register(ForNode(self.indent_level).add_body(iterator, condition, step, body_program_node.nodes))

    def is_separator_correct(self):
        parseRes = ParseResult()
        if self.current_token.type != TT_SEMI_COLON:
            return parseRes.failure(InvalidSyntaxError("Missing ';'.", self.current_token.pos))
        self.advance()
        return parseRes

    def is_syntax_correct(self):
        parseRes = ParseResult()
        self.indent_level = 0
        if self.current_token.type != TT_COLON:
            return parseRes.failure(InvalidSyntaxError("Missing ':'.", self.current_token.pos))
        self.advance()
        
        while self.current_token.type == TT_NEWLINE:
            self.advance()
        if self.current_token.type != TT_INDENT:
            return parseRes.failure(IndentationError("Found lower level of indentation.", self.current_token.pos))
        while self.current_token.type == TT_INDENT:
            self.advance()
            self.indent_level += 1
        if self.current_token.type == TT_INDENT:
            return parseRes.failure(IndentationError("Found higher level of indentation.", self.current_token.pos))
        return parseRes
    
    def get_bodies(self, indent):
        parseRes = ParseResult()
        program_node = ProgramNode()
        
        body_node = parseRes.register(self.expr())
        if parseRes.error: return parseRes
        program_node.addNode(body_node)
        print("IN BODIES: ", body_node, self.current_token)
        print(indent)
        while True:
            if self.pos + indent >= len(self.tokens) or self.tokens[self.pos + indent].type != TT_INDENT:
                break
            for i in range(indent):
                self.advance()
            
            self.advance()
            body_node = parseRes.register(self.expr())
            if parseRes.error: return parseRes
            program_node.addNode(body_node)
        return parseRes.success(program_node)
        
    def cond_expr(self):
        return self.bin_op(self.comp_expr, (TT_AND, TT_OR))
        
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
            left = parseRes.register(BinOpNode(left, op, right, self.indent_level))

        return left

    def comp_expr(self):
        parseRes = ParseResult()
        if self.current_token.type == TT_NOT:
            op_token = self.current_token
            self.advance()
            node = parseRes.register(self.comp_expr())
            return parseRes.register(UnaryOpNode(op_token, node, self.indent_level))
        node = parseRes.register(self.bin_op(self.arith_expr, COMP_OPS))
        if parseRes.error: return parseRes
        return node
    
    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS, TT_BIT_OR, TT_BIT_XOR))

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV, TT_MOD, TT_REMAINDER, TT_POWER, TT_BIT_AND))

    def factor(self):
        parseRes = ParseResult()
        token = self.current_token
        if token.type == TT_INDENT:
            self.indent_level += 1
        if token.type == TT_IDENTIFIER:
            token_identifier = self.current_token
            self.advance()
            return self.var_access(token_identifier)
        # PREFIX
        if token.type in (TT_PLUS, TT_MINUS, TT_BIT_NOT): 
            self.advance()
            factor = parseRes.register(self.factor())
            if parseRes.error: return parseRes
            return parseRes.register(UnaryOpNode(token, factor, self.indent_level))
        # POSTFIX
        if token.type in (TT_PLUS_PLUS): 
            factor = parseRes.register(self.factor())
            if parseRes.error: return parseRes
            self.advance()
            return parseRes.register(UnaryOpNode(token, factor, self.indent_level))
        if token.type == TT_LPAREN:
            self.advance()
            expr = parseRes.register(self.expr())
            if parseRes.error: return parseRes
            if self.current_token.type == TT_RPAREN:
                self.advance()
                return parseRes.register(expr)
            else:
                return parseRes.failure(InvalidSyntaxError("')' expected.", self.current_token.pos))
        if token.type in (TT_INT, TT_FLOAT):
            self.advance()
            return parseRes.register(NumberNode(token, self.indent_level))
        if token.type in (TT_DOUBLE_QUOTES, TT_SINGLE_QUOTES):
            self.advance()
            if self.current_token.type == TT_STRING:
                string_token = self.current_token
                self.advance()
                self.advance()
                return parseRes.register(StringNode(string_token, self.indent_level))
                
        if self.current_token.type == TT_EOF:
            return parseRes.failure(InvalidSyntaxError(f"Expression with missing terms found.", self.current_token.pos))

        return parseRes.failure(InvalidSyntaxError(f"Must be type integer or float, not '{self.current_token.value}'", self.current_token.pos))

    def var_update(self):
        parseRes = ParseResult()
        
        identifier_token = self.current_token
        
        if self.pos < len(self.tokens) - 1 and self.tokens[self.pos + 1].type in ASSIGNMENT_OPS + POSTFIX_UNARY + (TT_EQ,):
            self.advance()
            update_token = self.current_token
            self.advance()
            if update_token.type in ASSIGNMENT_OPS + (TT_EQ,):
                expr = parseRes.register(self.bin_op(self.comp_expr, (TT_AND, TT_OR)))
                if parseRes.error: return parseRes
                return parseRes.register(VarUpdateNode(identifier_token, expr, self.indent_level).add_update_token(update_token))
            if update_token.type in POSTFIX_UNARY:
                return parseRes.register(VarUpdateNode(identifier_token, NumberNode(Token(TT_INT, 1, self.current_token.pos), self.indent_level), self.indent_level).add_update_token(update_token))    

        return self.bin_op(self.comp_expr, (TT_AND, TT_OR))

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
        return parseRes.register(VarAssignNode(keyword, identifier_token, expr, self.indent_level))
    
    def var_access(self, identifier_token):
        parseRes = ParseResult()
        return parseRes.register(VarAccessNode(identifier_token, self.indent_level))
    
    
    