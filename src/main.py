from vacuole.lexer import Lexer
from vacuole.parser import Parser
from vacuole.interpreter import Interpreter, SymbolTable

from constants.tokens import *

def parse_input(text, line_number, symbol_table):
    fn = "input.txt"
    # Lexer
    lexer = Lexer(fn, text, line_number)
    tokens, error = lexer.tokenize()
    if error: return None, error
    print("Tokens: ", tokens)

    # Parser
    parser = Parser(fn, tokens)
    ast, error = parser.parse()
    if error: return None, error
    print("AST: ", ast)
    return ast, error

def run():
    text = ""
    with open("input.txt", "r") as f:
        text = f.read()

    print(text)
    symbol_table = SymbolTable()
    symbol_table.set_default_values()
    
    result, error = parse_input(text, 1, symbol_table)
    if error:
        print(error)
        return

    # Interpreter
    interpreter = Interpreter("input.txt", symbol_table)
    program = interpreter.visit(result)
    for output in program:
        if output.error:
            print(output.error)
        else:
            print(output.result)
    

if __name__ == "__main__":
    run()