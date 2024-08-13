from lexer import Lexer

def run(text):

    lexer = Lexer("<stdin>", text)
    tokens, error = lexer.tokenize()
    return tokens, error

if __name__ == "__main__":
    while True:
        text = input("vacuole > ")
        result, error = run(text)

        if error:
            print(error)
        else:
            print(result)
