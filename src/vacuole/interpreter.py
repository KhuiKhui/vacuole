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
    def update(self, identifier, value):
        get_value = self.symbols.get(identifier, None)
        if get_value == None: return None
        self.symbols[identifier].updateEntry(value)
        return value
    def setDefaultValues(self):
        self.set("true", "true", Number(1))
        self.set("false", "false", Number(0))
        self.set("null", "null", Number(0))
class SymbolTableEntry:
    def __init__(self, keyword, identifier, value) -> None:
        self.keyword = keyword
        self.identifier = identifier
        self.value = value
    def updateEntry(self, new_value):
        self.value = new_value
    

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
    
    def visit_ProgramNode(self, node):
        rt = RuntimeResult()
        processes = []
        for node in node.nodes:
            outputs = self.visit(node)
            if isinstance(outputs.result, list):
                for result in outputs.result:
                    processes.append(result)
            else:
                processes.append(outputs)
        return processes

    def visit_IfNode(self, node):
        rt = RuntimeResult()
        for case in node.cases:
            
            cond_result = rt.register(self.visit(case["condition"]))
            if rt.error: return rt
            if cond_result.number == 1:
                action = rt.register(self.visit(case["action"]))
                if rt.error: return rt
                return rt.success(action)

        return rt.success(None)
    
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
        elif node.op_token.type == TT_GREATER_THAN:
            result = lvalue.is_greater_than(rvalue)
        elif node.op_token.type == TT_GREATER_OR_EQ_TO:
            result = lvalue.is_greater_or_eq_to(rvalue)
        elif node.op_token.type == TT_LESS_THAN:
            result = lvalue.is_less_than(rvalue)
        elif node.op_token.type == TT_LESS_OR_EQ_TO:
            result = lvalue.is_less_or_eq_to(rvalue)
        elif node.op_token.type == TT_EQ_TO:
            result = lvalue.is_eq_to(rvalue)
        elif node.op_token.type == TT_NOT_EQ_TO:
            result = lvalue.is_not_eq_to(rvalue)
        elif node.op_token.type == TT_AND:
            result = lvalue.and_with(rvalue)
        elif node.op_token.type == TT_OR:
            result = lvalue.or_with(rvalue)
        elif node.op_token.type == TT_BIT_AND:
            result = lvalue.bit_and_with(rvalue)
        elif node.op_token.type == TT_BIT_OR:
            result = lvalue.bit_or_with(rvalue)
        
        return rt.success(result)
    def visit_UnaryOpNode(self, node):
        rt = RuntimeResult()
        value = rt.register(self.visit(node.node))
        if node.op_token.type == TT_PLUS:
            result = value
        if node.op_token.type == TT_MINUS:
            result = value.mul_by(Number(-1))
        if node.op_token.type == TT_NOT:
            result = value.not_op()
        return rt.success(result)
    
    def visit_NumberNode(self, node):
        rt = RuntimeResult()
        number = Number(node.token.value)
        return rt.success(number)

    def visit_VarAssignNode(self, node):
        rt = RuntimeResult()
        value = rt.register(self.visit(node.node))
        if rt.error: return rt
        self.symbol_table.set(node.keyword, node.identifier_token.value, value)
        return rt.success(value)
    
    def visit_VarUpdateNode(self, node):
        rt = RuntimeResult()
        value = rt.register(self.visit(node.node))
        if rt.error: return rt
        if self.symbol_table.get(node.identifier_token.value) == None:
            return rt.failure(RuntimeError(f'{node.identifier_token.value} is not defined.', node.identifier_token.pos))
        self.symbol_table.update(node.identifier_token.value, value)
        return rt.success(value)
    
    def visit_VarAccessNode(self, node):
        rt = RuntimeResult()
        var_value_entry = self.symbol_table.get(node.identifier_token.value)
        if var_value_entry == None:
            return rt.failure(RuntimeError(f'{node.identifier_token.value} is not defined.', node.identifier_token.pos))
        return rt.success(var_value_entry.value)