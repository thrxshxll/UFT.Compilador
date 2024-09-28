from lex import Lex
import rules
import sys


with open(sys.argv[1], mode='r') as codefile:
    code = ''
    for line in codefile:
        code += ''.join(line)

# print('parsing content')
content = code
print(content)
print('\n')

lex = Lex(content, [ \
    rules.KeywordRule(), \
    rules.CommentRule(), \
    rules.OperatorRule(), \
    rules.DelimiterRule(), \
    rules.IntConstantRule(), \
    rules.FloatConstantRule(), \
    rules.TextConstantRule(), \
    rules.IdRule() ])


while True:
    token_atual = lex.next()
    if token_atual is None:
        break
    print(f'token extraido: {token_atual}\n\n')
