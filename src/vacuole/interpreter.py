from vacuole.values.number import *
from vacuole.values.string import *
from vacuole.errors import *
from vacuole.validator import *
from vacuole.assigner import *
from constants.tokens import *
from vacuole.nodes import *

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
        self.symbols[identifier].update_entry(value)
        return value
    def set_default_values(self):
        self.set("true", "true", Number(1))
        self.set("false", "false", Number(0))
        self.set("null", "null", Number(0))
class SymbolTableEntry:
    def __init__(self, keyword, identifier, value) -> None:
        self.keyword = keyword
        self.identifier = identifier
        self.value = value
    def update_entry(self, new_value):
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
                for output in outputs.result:
                    if output != None:
                        processes.append(rt.success(output))
            else:
                processes.append(outputs)
        return processes

    def visit_IfNode(self, node):
        rt = RuntimeResult()
        cases = node.cases

        for case in cases:
            cond_result = rt.register(self.visit(case["condition"]))
            if rt.error: return rt

            # If cond_result is True
            if cond_result.value == 1:
                body = case["body"]
                body_result = []
                for i in body:
                    action = rt.register(self.visit(i))
                    if rt.error: return rt
                    if isinstance(action, list):
                        for j in action:
                            body_result.append(j)
                    else:
                        body_result.append(action)
                return rt.success(body_result)
        return rt.success(None)
    
    def visit_ForNode(self, node):
        rt = RuntimeResult()
        loop = node.loop
        header = loop["header"]
        body = loop["body"]
        
        iterator = rt.register(self.visit(header["iterator"]))
        condition = rt.register(self.visit(header["condition"]))

        if rt.error: return rt

        if condition.value == 1:
            body_result = []
            subseq_condition = rt.register(self.visit(header["condition"]))
            if rt.error: return rt
            while subseq_condition.value == 1:
                for i in body:
                    action = rt.register(self.visit(i))
                    if rt.error: return rt
                    if isinstance(action, list):
                        for j in action:
                            body_result.append(rt.register(j))
                    else:
                        body_result.append(rt.register(action))
                self.visit(header["step"])
                subseq_condition = rt.register(self.visit(header["condition"]))
            return rt.success(body_result)
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
            if isinstance(lvalue, (String, Number)) and not isinstance(rvalue, Number):
                return rt.failure(RuntimeError("Illegal multiplication expression.", node.op_token.pos))
                
            result = lvalue.mul_by(rvalue)
        elif node.op_token.type == TT_DIV:
            if rvalue.value == 0:
                return rt.failure(RuntimeError("Division by zero.", node.op_token.pos))
            result = lvalue.div_by(rvalue)
        elif node.op_token.type == TT_POWER:
            result = lvalue.raise_power(rvalue)
        elif node.op_token.type == TT_MOD:
            result = lvalue.mod(rvalue)
        elif node.op_token.type == TT_REMAINDER:
            result = lvalue.get_remainder(rvalue)
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
        elif node.op_token.type == TT_BIT_XOR:
            result = lvalue.bit_xor_with(rvalue)
        
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
        if node.op_token.type == TT_BIT_NOT:
            result = value.bit_not_op()
        return rt.success(result)
    
    def visit_NumberNode(self, node):
        rt = RuntimeResult()
        number = Number(node.token.value)
        return rt.success(number)

    def visit_StringNode(self, node):
        rt = RuntimeResult()
        string = String(node.token.value)
        return rt.success(string)

    def visit_VarAssignNode(self, node):
        rt = RuntimeResult()
        validator = Validator()
        value = rt.register(self.visit(node.node))
        if rt.error: return rt
        if not validator.isValidDataType(node.keyword, value):
            return rt.failure(TypeError(f"'{value}' incorrectly assigned to type '{node.keyword}'", node.identifier_token.pos))
        self.symbol_table.set(node.keyword, node.identifier_token.value, value)
        return rt.success(node.identifier_token.value)
    
    def visit_VarUpdateNode(self, node):
        rt = RuntimeResult()
        identifier = node.identifier_token.value
        if self.symbol_table.get(identifier) == None:
            return rt.failure(RuntimeError(f'{identifier} is not defined.', node.identifier_token.pos))

        base_value = self.symbol_table.get(identifier).value
        
        updated_value = rt.register(self.visit(node.node))
        if rt.error: return rt
        if node.update_token.type in ASSIGNMENT_OPS:
            if node.update_token.type == TT_PLUS_ASSIGN:
                updated_value = base_value.add_to(updated_value)
            if node.update_token.type == TT_MINUS_ASSIGN:
                updated_value = base_value.sub_by(updated_value)
            if node.update_token.type == TT_MUL_ASSIGN:
                updated_value = base_value.mul_by(updated_value)
            if node.update_token.type == TT_DIV_ASSIGN:
                updated_value = base_value.div_by(updated_value)
        if node.update_token.type in POSTFIX_UNARY:
            if node.update_token.type == TT_PLUS_PLUS:
                updated_value = base_value.add_to(updated_value)
            if node.update_token.type == TT_MINUS_MINUS:
                updated_value = base_value.sub_by(updated_value)
        self.symbol_table.update(node.identifier_token.value, updated_value)
        return rt.success(None)
    
    def visit_VarAccessNode(self, node):
        rt = RuntimeResult()
        var_value_entry = self.symbol_table.get(node.identifier_token.value)
        if var_value_entry == None:
            return rt.failure(RuntimeError(f'{node.identifier_token.value} is not defined.', node.identifier_token.pos))
        return rt.success(var_value_entry.value)