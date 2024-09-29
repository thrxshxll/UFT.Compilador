from lex import Lex
import sys


with open(sys.argv[1], mode='r') as codefile:
    code = ''
    for line in codefile:
        code += ''.join(line)

print('scanner content')
content = code
print(content, end='\n\n')

lex = Lex(content)

while True:
    token_atual = lex.next()
    if token_atual is None:
        break
    print(f'{token_atual}\n')
