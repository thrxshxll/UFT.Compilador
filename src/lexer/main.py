from lex import Lex
import sys

def fopen(codefile):
    with open(codefile, mode='r') as file:
        return file.read()


if __name__ == '__main__':

    if len(sys.argv) < 2:
        raise ValueError('Passe o arquivo para o Lexer')

    code = fopen(sys.argv[1])

    lex = Lex(code)

    while True:
        token_atual = lex.next()
        if token_atual is None:
            break
        print(f'{token_atual}\n')