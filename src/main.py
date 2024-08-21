from vacuole.lexer import Lexer
from vacuole.parser import Parser
from vacuole.interpreter import Interpreter, SymbolTable

from constants.tokens import *

def run(text, line_number, symbol_table):
    fn = "<stdin>"
    # Lexer
    lexer = Lexer(fn, text, line_number)
    tokens, error = lexer.tokenize()
    if error: return None, error
    print("Tokens: ", tokens, tokens[0])

    # Parser
    parser = Parser(fn, tokens)
    ast, error = parser.parse()
    if error: return None, error
    print("AST: ", ast)

    # Interpreter
    interpreter = Interpreter(fn, symbol_table)
    output = interpreter.visit(ast)
    return output.result, output.error

# if __name__ == "__main__":
#     text = []
#     with open("input.txt", "r") as f:
#         text = f.read().strip("\n").split("\n")
#         text = [i for i in text if i != '']
    
#     symbol_table = SymbolTable()
#     symbol_table.setDefaultValues()
    
#     for i in range(len(text)):
#         result, error = run(text[i], i+1, symbol_table)

#         if error:
#             print(error)
#         else:
#             print(result)

if __name__ == "__main__":
    symbol_table = SymbolTable()
    symbol_table.setDefaultValues()
    
    while True:
        text = input("vacuole > ")
        result, error = run(text, 1, symbol_table)

        if error:
            print(error)
        else:
            print(result)