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
    parser.program()