from vacuole.lexer import Lexer
from vacuole.parser import Parser

from constants.tokens import *

def run(text):

    lexer = Lexer("<stdin>", text)
    tokens, error = lexer.tokenize()
    if error: return [], error
    parser = Parser("<stdin>", tokens)
    ast, error = parser.parse()
    return ast, error

if __name__ == "__main__":
    while True:
        text = input("vacuole > ")
        result, error = run(text)

        if error:
            print(error)
        else:
            print(result)
