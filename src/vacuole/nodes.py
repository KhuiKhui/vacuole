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
    

    
