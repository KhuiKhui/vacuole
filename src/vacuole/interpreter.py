from vacuole.values.number import Number
from vacuole.errors import *
from constants.tokens import *

#rt.failure(RuntimeError(f"{identifier} is not defined.", pos))
class SymbolTable:
    def __init__(self) -> None:
        self.symbols = {}
        self.parent = None
    def get(self, identifier):
        value = self.symbols.get(identifier, None)
        if value == None and self.parent != None:
            return self.parent.get(identifier)
        return value
    def set(self, keyword, identifier, value):
        self.symbols[identifier] = SymbolTableEntry(keyword, identifier, value)

class SymbolTableEntry:
    def __init__(self, keyword, identifier, value) -> None:
        self.keyword = keyword
        self.identifier = identifier
        self.value = value
    

class RuntimeResult:
    def __init__(self) -> None:
        self.result = None
        self.error = None
    def register(self, res):
        if isinstance(res, RuntimeResult):
            if res.error: self.error = res.error
            return res.result
        return res
    def success(self, res):
        self.result = res
        return self
    def failure(self, error):
        self.error = error
        return self

class Interpreter:
    def __init__(self, fn, symbol_table) -> None:
        self.fn = fn
        self.symbol_table = symbol_table
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit)
        return method(node)

    def no_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')
    
    def visit_VarAssignNode(self, node):
        rt = RuntimeResult()
        value = rt.register(self.visit(node.node))
        if rt.error: return rt
        self.symbol_table.set(node.keyword, node.identifier, value)
        return rt.success(value)
    
    def visit_VarAccessNode(self, node):
        rt = RuntimeResult()
        var_value_entry = self.symbol_table.get(node.token.value)
        if var_value_entry == None:
            return rt.failure(RuntimeError(f'{node.token.value} is not defined.', node.token.pos))
        return rt.success(var_value_entry.value)

    def visit_NumberNode(self, node):
        rt = RuntimeResult()
        number = Number(node.token.value)
        return rt.success(number)
    
    def visit_BinOpNode(self, node):
        rt = RuntimeResult()
        lvalue = rt.register(self.visit(node.lnode))
        if rt.error: return rt
        rvalue = rt.register(self.visit(node.rnode))
        if rt.error: return rt
        if node.op_token.type == TT_PLUS:
            result = lvalue.add_to(rvalue)
        elif node.op_token.type == TT_MINUS:
            result = lvalue.sub_by(rvalue)
        elif node.op_token.type == TT_MUL:
            result = lvalue.mul_by(rvalue)
        elif node.op_token.type == TT_DIV:
            if rvalue.number == 0:
                return rt.failure(RuntimeError("Division by zero", node.op_token.pos))
            result = lvalue.div_by(rvalue)
        elif node.op_token.type == TT_POWER:
            result = lvalue.raise_power(rvalue)
        elif node.op_token.type == TT_MOD:
            result = lvalue.mod(rvalue)
        
        return rt.success(result)
    def visit_UnaryOpNode(self, node):
        rt = RuntimeResult()
        value = rt.register(self.visit(node.node))
        if node.op_token.type == TT_PLUS:
            result = value
        if node.op_token.type == TT_MINUS:
            result = value.mul_by(Number(-1))
        return rt.success(result)
