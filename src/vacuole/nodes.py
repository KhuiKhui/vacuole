
class ProgramNode:
    def __init__(self) -> None:
        self.nodes = []
    def __repr__(self) -> str:
        return f'{self.nodes}'
    def addNode(self, node):
        self.nodes.append(node)
        return self

class IfNode:
    def __init__(self, indent_level) -> None:
        self.cases = [] # Must be list because there are else if and else cases too
        self.indent_level = indent_level
    def __repr__(self) -> str:
        return f'IF: {self.cases}'
    def add_body(self, condition, body):
        case = {'condition': None, 'body': []}
        case['condition'] = condition
        if isinstance(body, list):
            for i in body:
                case["body"].append(i)
        else:
            case["body"].append(body)
        self.cases.append(case)
        return self

class ForNode:
    def __init__(self, indent_level) -> None:
        self.loop = {'header': {'iterator': None, 'condition': None, 'step': None}, 'body': []}
        self.indent_level = indent_level
    def __repr__(self) -> str:
        return f"FOR: {self.loop}"
    def add_body(self, iterator, condition, step, body):
        self.loop['header']['iterator'] = iterator
        self.loop['header']['condition'] = condition
        self.loop['header']['step'] = step

        if isinstance(body, list):
            for i in body:
                self.loop["body"].append(i)
        else:
            self.loop["body"].append(body)
        return self
class BinOpNode:
    def __init__(self, lnode, op_token, rnode, indent_level) -> None:
        self.op_token = op_token
        self.lnode = lnode
        self.rnode = rnode
        self.indent_level = indent_level
    def __repr__(self) -> str:
        return f'({self.lnode} {self.op_token} {self.rnode})'
    
class UnaryOpNode:
    def __init__(self, op_token, node, indent_level) -> None:
        self.op_token = op_token
        self.node = node
        self.indent_level = indent_level
    def __repr__(self) -> str:
        return f'({self.op_token} {self.node})'
    
class NumberNode:
    def __init__(self, token, indent_level) -> None:
        self.token = token
        self.indent_level = indent_level
    def __repr__(self) -> str:
        return f'{self.token}'

class StringNode:
    def __init__(self, token, indent_level) -> None:
        self.token = token
        self.indent_level = indent_level
    def __repr__(self) -> str:
        return f'{self.token}'

class VarAssignNode:
    def __init__(self, keyword, identifier_token, node, indent_level) -> None:
        self.keyword = keyword
        self.identifier_token = identifier_token
        self.node = node
        self.indent_level = indent_level
    def __repr__(self) -> str:
        return f'{self.keyword} {self.identifier_token} = {self.node}'
    
class VarUpdateNode:
    def __init__(self, identifier_token, node, indent_level) -> None:
        self.identifier_token = identifier_token
        self.node = node
        self.indent_level = indent_level
    def __repr__(self) -> str:
        return f'{self.identifier_token} = {self.node}'
    
class VarAccessNode:
    def __init__(self, identifier_token, indent_level) -> None:
        self.identifier_token = identifier_token
        self.indent_level = indent_level
    def __repr__(self) -> str:
        return f'{self.identifier_token}'