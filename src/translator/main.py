from lex import Lex
from translator import Translator
import sys


def fopen(filename: str) -> str:
    with open(filename, mode='r') as file:
        return file.read()


if __name__ == '__main__':

    if len(sys.argv) < 2:
        raise ValueError('Passe o código-fonte como argumento para o Compilador')

    code = fopen(sys.argv[1])

    parser = Translator(code)
    parser.program()