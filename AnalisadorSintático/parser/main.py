from lex import Lex
from parser import Parser

import sys


def openFile(filename: str) -> str:
    with open(filename, mode='r') as codefile:
        code = ''
        for line in codefile:
            code += ''.join(line)
    return code


if __name__ == '__main__':

    code = openFile(sys.argv[1])

    parser = Parser(code)
    parser.analisar()




    # lex = Lex(code)

    # while True:
    #     token_atual = lex.next()
    #     if token_atual is None:
    #         break
    #     print(token_atual)