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

class NumberNode:
    def __init__(self, token, indent_level) -> None:
        self.token = token
        self.indent_level = indent_level
    def __repr__(self) -> str:
        return f'{self.token}'
    
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
    
class IfNode:
    def __init__(self, indent_level) -> None:
        self.cases = []
        self.action_nodes = []
        self.indent_level = indent_level
    def __repr__(self) -> str:
        return f'{self.cases} {self.action_nodes}'
    def addCase(self, case):
        self.cases.append(case)
        return self
    def addActionNode(self, action_node):
        self.action_nodes.append(action_node)
        return self
