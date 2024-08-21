from vacuole.lexer import Lexer
from vacuole.parser import Parser
from vacuole.interpreter import Interpreter, SymbolTable

from constants.tokens import *

def run(text, symbol_table):
    fn = "<stdin>"
    # Lexer
    lexer = Lexer(fn, text)
    tokens, error = lexer.tokenize()
    if error: return None, error
    print("Tokens: ", tokens)

    # Parser
    parser = Parser(fn, tokens)
    ast, error = parser.parse()
    if error: return None, error
    print("AST: ", ast)

    # Interpreter
    interpreter = Interpreter(fn, symbol_table)
    output = interpreter.visit(ast)
    return output.result, output.error

if __name__ == "__main__":
    symbol_table = SymbolTable()
    symbol_table.setDefaultValues()
    
    while True:
        text = input("vacuole > ")
        result, error = run(text, symbol_table)

        if error:
            print(error)
        else:
            print(result)
