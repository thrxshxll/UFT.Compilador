from lex import Lex
from token import TokenClass


class Translator:
    def __init__(self, codigoFonte: str, ):
        self.codigoFonte = Lex(codigoFonte).code2tokens()       # uma lista com todas as palavras do código já classificadas
        self.atualToken = None                                  #
        self.debugIdent = 0                                     #
        self.blockIdent = 0


    def testarClasse(self, *token_classes):
        """
            Testa se o Token atual pertence às classes passadas como argumento em '*token_classes'.
        """

        # print(self.debugIdent * ' ' + f'? testando classes {token_classes} => {self.atualToken}')
        
        if self.atualToken is None:
            return False

        result = (self.atualToken.token_value in token_classes) or (self.atualToken.token_class in token_classes)
        
        return result

    
    def validarClasse(self, *token_classes):

        # print(self.debugIdent * ' ' + f'! validando classes {token_classes} => {self.atualToken}')
        
        if self.atualToken is None:
            raise SyntaxError('Unexpected end of input.')

        if (self.atualToken.token_value in token_classes) or (self.atualToken.token_class in token_classes):
            token_value = self.atualToken.token_value
            self.proximoToken()
            return token_value
        else:
            raise SyntaxError('Unexpected token {}. Expected one of: {}'.format(self.atualToken.token_class, token_classes))


    def dbprint(self, msg: str):
        print(self.debugIdent * ' ' + msg)


    def proximoToken(self):
        if len(self.codigoFonte) > 0:
            self.atualToken = self.codigoFonte.pop(0)
        # else:
            # self.atualToken = None

    
    def program(self):
        
        self.proximoToken()
        
        print(self.block())

        self.validarClasse(TokenClass.EOF)


    def block(self):
        
        if self.atualToken is None:
            return

        ret = ''
        if self.testarClasse('CONST'):
            ret += self.constants()
        if self.testarClasse('VAR'):
            ret += self.variables()
        if self.testarClasse('PROCEDURE'):
            ret += self.procedures()
        if self.testarClasse(TokenClass.IDENTIFIER,'CALL', 'BEGIN','IF','WHILE','PRINT'):
            ret += self.statement()
        return ret


    def constants(self):

        self.validarClasse('CONST')
        tmp = self.constdecl()
        self.validarClasse(';')
        return f'{tmp}\n'

    
    def variables(self):

        self.validarClasse('VAR')
        tmp = self.vardecl()
        self.validarClasse(';')
        return f'{tmp}\n'
        


    def procedures(self):

        tmp = f'\n{self.procdecl()}\n'
        if self.testarClasse('PROCEDURE'):
            tmp += self.procedures()
        return tmp
            


    def statement(self):

        if self.testarClasse(TokenClass.IDENTIFIER):
            id = self.validarClasse(TokenClass.IDENTIFIER)
            self.validarClasse('<-')
            exp = self.expression()
            return f'{id} = {exp}\n'

        elif self.testarClasse('CALL'):
            self.validarClasse('CALL')
            ret = self.validarClasse(TokenClass.IDENTIFIER)
            _args = ''
            if self.testarClasse(TokenClass.IDENTIFIER, TokenClass.NUMBER):
                _args += self.argdecl()

            if len(_args) > 0:
                return f'{ret}({_args})\n'

            return f'{ret}()\n'

        elif self.testarClasse('IF'):
            self.validarClasse('IF')
            
            ret = self.blockIdent*' '
            
            self.blockIdent += 4
            
            _condition = ''
            if self.testarClasse('NOT'):
                self.validarClasse('NOT')
                _condition += 'not '
            _condition += self.condition()
            self.validarClasse('THEN')
            _stmt = self.statement()


            ret += f'if {_condition}:\n' + _stmt

            self.blockIdent -= 4
            return ret

        elif self.testarClasse('WHILE'):
            self.validarClasse('WHILE')

            ret = self.blockIdent*' '

            self.blockIdent += 4
            
            _condition = ''
            if self.testarClasse('NOT'):
                self.validarClasse('NOT')
                _condition += 'not '
            _condition += self.condition()
            self.validarClasse('DO')
            _stmt = self.statement()
            ret += f'while {_condition}:\n' + _stmt
            
            self.blockIdent -= 4
            return ret
            

        elif self.testarClasse('PRINT'):
            self.validarClasse('PRINT')
            tmp = self.expression()
            return f'print({tmp})\n'


        elif self.testarClasse('BEGIN'):
            self.validarClasse('BEGIN')
            tmp = self.compound_stmt()
            self.validarClasse('END')
            return tmp


    def compound_stmt(self):

        if self.testarClasse(TokenClass.IDENTIFIER,'CALL','BEGIN','PRINT'):
            tmp = self.blockIdent*' ' + self.statement()
        else:
            tmp = self.statement()
            
        self.validarClasse(';')
        if self.testarClasse(TokenClass.IDENTIFIER,'CALL', 'IF', 'WHILE','BEGIN','PRINT'):
            tmp += self.compound_stmt()

        return tmp


    def constdecl(self):
        
        if self.testarClasse(TokenClass.IDENTIFIER):
            tmp = self.constdef()
        if self.testarClasse(','):
            self.validarClasse(',')
            tmp += '\n' + self.constdecl()
        return self.blockIdent*' ' + tmp
            

    def vardecl(self):
        
        ret = f'{self.validarClasse(TokenClass.IDENTIFIER)} = 0'
        if self.testarClasse(','):
            self.validarClasse(',')
            ret += f'\n{self.vardecl()}'
        return self.blockIdent*' ' + ret
    

    def argdecl(self):
        
        ret = f'{self.validarClasse(TokenClass.IDENTIFIER)}'
        if self.testarClasse(','):
            ret += self.validarClasse(',') + ' '
            ret += f'{self.argdecl()}'
        return ret
            

    def procdecl(self):

        self.blockIdent += 4

        self.validarClasse('PROCEDURE')
        _id = self.validarClasse(TokenClass.IDENTIFIER)
        _args = ''
        if self.testarClasse(TokenClass.IDENTIFIER, TokenClass.NUMBER):
            _args += self.argdecl()
        self.validarClasse(';')
        _block = self.block()
        self.validarClasse(';')

        if len(_args) > 0:
            _def = f'def {_id}({_args}):\n' + _block
        else:
            _def = f'def {_id}():\n' + _block

        self.blockIdent -= 4
        return _def

        
    
    def constdef(self):

        _id = self.validarClasse(TokenClass.IDENTIFIER)
        _re = self.validarClasse('=')
        _num = self.validarClasse(TokenClass.NUMBER)

        return f'{_id} = {_num}'
        

    def condition(self):

        if self.testarClasse('ODD'):
            self.validarClasse('ODD')
            _exp = self.expression()
            return f'{_exp} % 2 != 0'

        if self.testarClasse('EVEN'):
            self.validarClasse('EVEN')
            _exp = self.expression()
            return f'{_exp} % 2 == 0'

        else:
            _exp1 = self.expression()
            _re = self.relation()
            _exp2 = self.expression()

            if '%' in _re:
                return f'{_exp1}{_re}{_exp2} == 0'

            return f'{_exp1}{_re}{_exp2}'


    def relation(self):

        ret = self.validarClasse('=', '#', '<', '<=', '>', '>=', '/?')

        if ret == '/?':
            ret = '%'
        elif ret == '=':
            ret = '=='
            
        return f' {ret} '


    def expression(self):

        ret = ''
        if self.testarClasse('+','-'):
            ret += self.sign()

        ret += self.term()

        if self.testarClasse('+', '-'):
            ret += self.sign()
            ret += self.term()
        return ret
        

    def sign(self):
        ret = self.validarClasse('+', '-')
        return f' {ret} '


    def term(self):

        ret = self.factor()

        if self.testarClasse('/', '*'):
            ret += self.factors()
        return f'{ret}'


    def factor(self):

        if self.testarClasse(TokenClass.IDENTIFIER):
            tmp = self.validarClasse(TokenClass.IDENTIFIER)

        elif self.testarClasse(TokenClass.NUMBER):
            tmp = self.validarClasse(TokenClass.NUMBER)            

        elif self.testarClasse('('):
            tmp = self.validarClasse('(')
            tmp += self.expression()
            tmp += self.validarClasse(')')
        return tmp
            

    def factors(self):

        ret = f" {self.validarClasse('/', '*')} "

        ret += self.factor()
        return ret