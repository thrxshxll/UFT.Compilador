from parser import Parser

import sys


def fopen(filename: str):
    with open(filename, mode='r') as file:
        return file.read()


if __name__ == '__main__':

    if len(sys.argv) < 2:
        raise ValueError('Passe o arquivo para o Parser')

    code = fopen(sys.argv[1])

    parser = Parser(code)
    parser.program()