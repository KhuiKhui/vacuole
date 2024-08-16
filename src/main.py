from vacuole.lexer import Lexer
from vacuole.parser import Parser
from vacuole.interpreter import Interpreter

from constants.tokens import *

def run(text):
    fn = "<stdin>"
    # Lexer
    lexer = Lexer(fn, text)
    tokens, error = lexer.tokenize()
    if error: return None, error

    # Parser
    parser = Parser(fn, tokens)
    ast, error = parser.parse()
    if error: return None, error

    # Interpreter
    interpreter = Interpreter(fn)
    output = interpreter.visit(ast)
    return output.result, output.error

if __name__ == "__main__":
    while True:
        text = input("vacuole > ")
        result, error = run(text)

        if error:
            print(error)
        else:
            print(result)
