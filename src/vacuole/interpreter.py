from vacuole.values.number import Number
from vacuole.errors import *
from constants.tokens import *

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
    def __init__(self, fn) -> None:
        self.fn = fn
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit)
        return method(node)

    def no_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node):
        rt = RuntimeResult()
        number = Number(node.token.value)
        #number.set_pos(node.token.start, node.token.end)
        return rt.success(number)
    
    def visit_BinOpNode(self, node):
        print("Found binary op node!")
        rt = RuntimeResult()
        lvalue = rt.register(self.visit(node.lnode))
        if rt.error: return rt
        rvalue = rt.register(self.visit(node.rnode))
        if rt.error: return rt
        if node.op_token.type == TT_PLUS:
            result = lvalue.add_to(rvalue)
        if node.op_token.type == TT_MINUS:
            result = lvalue.sub_by(rvalue)
        if node.op_token.type == TT_MUL:
            result = lvalue.mul_by(rvalue)
        if node.op_token.type == TT_DIV:
            if rvalue.number == 0:
                return rt.failure(RuntimeError("Division by zero", node.op_token.line, node.rnode.token.end, self.fn))
            result = lvalue.div_by(rvalue)
        if node.op_token.type == TT_POWER:
            result = lvalue.raise_power(rvalue)
        return rt.success(result)
        #return result.set_pos(node.lnode.token.start, node.lnode.token.end)
    def visit_UnaryOpNode(self, node):
        print("Found unary op node!")
        rt = RuntimeResult()
        value = rt.register(self.visit(node.node))
        if node.op_token.type == TT_PLUS:
            result = value
        if node.op_token.type == TT_MINUS:
            result = value.mul_by(Number(-1))
        return rt.success(result)
        #return result.set_pos(node.node.token.start, node.node.token.end)
