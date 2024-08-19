class VarAssignNode:
    def __init__(self, keyword, identifier, node) -> None:
        self.keyword = keyword
        self.identifier = identifier
        self.node = node
    def __repr__(self) -> str:
        return f'{self.keyword} {self.identifier} = {self.node}'
    
class VarAccessNode:
    def __init__(self, token) -> None:
        self.token = token
    def __repr__(self) -> str:
        return f'{self.token}'

class NumberNode:
    def __init__(self, token) -> None:
        self.token = token
    def __repr__(self) -> str:
        return f'{self.token}'
    
class BinOpNode:
    def __init__(self, lnode, op_token, rnode) -> None:
        self.op_token = op_token
        self.lnode = lnode
        self.rnode = rnode
    def __repr__(self) -> str:
        return f'({self.lnode} {self.op_token} {self.rnode})'
    
class UnaryOpNode:
    def __init__(self, op_token, node) -> None:
        self.op_token = op_token
        self.node = node
    def __repr__(self) -> str:
        return f'({self.op_token} {self.node})'

