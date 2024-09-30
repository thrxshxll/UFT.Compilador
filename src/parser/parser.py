from lex import Lex
from token import TokenClass


class Parser:
    def __init__(self, codigoFonte: str, ):
        self.codigoFonte = Lex(codigoFonte).code2tokens()       # uma lista com todas as palavras do código já classificadas
        self.atualToken = None                                  #
        self.debugIdent = 0                                     #


    def testarClasse(self, *token_classes):
        """
            Testa se o Token atual pertence às classes passadas como argumento em '*token_classes'.
        """

        print(self.debugIdent * ' ' + f'? testando classes {token_classes} => {self.atualToken}')
        
        if self.atualToken is None:
            return False

        result = (self.atualToken.token_value in token_classes) or (self.atualToken.token_class in token_classes)
        
        return result

    
    def validarClasse(self, *token_classes):

        print(self.debugIdent * ' ' + f'! validando classes {token_classes} => {self.atualToken}')
        
        if self.atualToken is None:
            raise SyntaxError('Unexpected end of input.')

        if self.atualToken.token_value or self.atualToken.token_class in token_classes:
            self.proximoToken()
        else:
            raise SyntaxError('Unexpected token {}. Expected one of: {}'.format(self.atualToken.token_class, token_classes))


    def dbprint(self, msg: str):
        print(self.debugIdent * ' ' + msg)


    def proximoToken(self):
        if len(self.codigoFonte) > 0:
            self.atualToken = self.codigoFonte.pop(0)

    
    def program(self):
        self.dbprint('> program()')
        
        self.proximoToken()
        
        self.block()

        self.dbprint('< program()')

        if self.atualToken.token_class == TokenClass.EOF:
            return
        
        
    def block(self):
        self.debugIdent += 1
        self.dbprint('> block()')
        
        if self.atualToken is None:
            return

        if self.testarClasse('CONST'):
            self.constants()
        elif self.testarClasse('VAR'):
            self.variables()
        elif self.testarClasse('PROCEDURE'):
            self.procedures()
        elif self.testarClasse(TokenClass.IDENTIFIER,
                             'CALL',
                             'BEGIN',
                             'IF',
                             'WHILE',
                             'PRINT'):
            self.compound_stmt()

        
        self.dbprint('< block()')
        self.debugIdent -= 1


    def constants(self):
        self.debugIdent += 1
        self.dbprint('> constants()')

        self.validarClasse('CONST')
        self.constdecl()
        self.validarClasse(';')

        self.dbprint('< constant()')
        self.debugIdent -= 1

    
    def variables(self):
        self.debugIdent += 1
        self.dbprint('> variables()')

        self.validarClasse('VAR')
        self.vardecl()
        self.validarClasse(';')
        
        self.dbprint('< variables()')
        self.debugIdent -= 1


    def procedures(self):
        self.debugIdent += 1
        self.dbprint('> procedures()')

        self.validarClasse('PROCEDURE')
        self.validarClasse(TokenClass.IDENTIFIER)
        self.validarClasse(';')
        self.block()
        self.validarClasse(';')
            
        self.dbprint('< procedures()')
        self.debugIdent -= 1


    def statement(self):
        self.debugIdent += 1
        self.dbprint('> statement()')

        if self.testarClasse(TokenClass.IDENTIFIER):
            self.validarClasse(TokenClass.IDENTIFIER)
            self.validarClasse('<-')
            self.expression()

        elif self.testarClasse('CALL'):
            self.validarClasse('CALL')
            self.validarClasse(TokenClass.IDENTIFIER)

        elif self.testarClasse('IF'):
            self.validarClasse('IF')
            if self.testarClasse('NOT'):
                self.validarClasse('NOT')
            self.condition()
            self.validarClasse('THEN')
            self.statement()

        elif self.testarClasse('WHILE'):
            self.validarClasse('WHILE')
            if self.testarClasse('NOT'):
                self.validarClasse('NOT')
            self.condition()
            self.validarClasse('DO')
            self.statement()

        elif self.testarClasse('PRINT'):
            self.validarClasse('PRINT')
            self.expression()

        elif self.testarClasse('BEGIN'):
            self.validarClasse('BEGIN')
            self.compound_stmt()
            self.validarClasse('END')
            
        self.dbprint('< statement()')
        self.debugIdent -= 1


    def compound_stmt(self):
        self.debugIdent += 1
        self.dbprint('> compound_stmt()')


        self.statement()
        self.validarClasse(';')
        if self.testarClasse(TokenClass.IDENTIFIER,
                             'CALL',
                             'IF',
                             'WHILE',
                             'PRINT',
                             'BEGIN',):
            self.compound_stmt()
        self.dbprint('< compound_stmt()')
        self.debugIdent -= 1


    def constdecl(self):
        
        self.debugIdent += 1
        self.dbprint('> constdecl()')
        self.constdef()
        if self.testarClasse(','):
            self.validarClasse(',')
            self.constdecl()
            
        self.dbprint('< constdecl()')
        self.debugIdent -= 1


    def vardecl(self):
        self.debugIdent += 1
        self.dbprint('> vardecl()')
        
        self.validarClasse(TokenClass.IDENTIFIER)
        
        if self.testarClasse(','):
            self.validarClasse(',')
            self.vardecl()
            
        self.dbprint('< vardecl()')
        self.debugIdent -= 1


    def procdecl(self):
        self.debugIdent += 1
        self.dbprint('> procdecl()')

        self.validarClasse('PROCEDURE')
        self.validarClasse(TokenClass.IDENTIFIER)
        self.validarClasse(';')
        self.block()
        self.validarClasse(';')

        self.dbprint('< procdecl()')
        self.debugIdent -= 1
        

    
    def constdef(self):
        self.debugIdent += 1
        self.dbprint('> constdef()')

        self.validarClasse(TokenClass.IDENTIFIER)
        self.validarClasse('=')
        self.validarClasse(TokenClass.NUMBER)

        self.dbprint('< constdef()')
        self.debugIdent -= 1
        

    def condition(self):
        self.debugIdent += 1
        self.dbprint('> condition()')

        if self.testarClasse('ODD'):
            self.expression()
        elif self.testarClasse('VEN'):
            self.expression()
        else:
            self.expression()
            self.relation()
            self.expression()

        self.debugIdent -= 1
        self.dbprint('< condition()')


    def relation(self):
        self.debugIdent += 1
        self.dbprint('> relation()')

        self.validarClasse('=',
                           '#',
                           '<',
                           '<=',
                           '>',
                           '>=',
                           '/?')

        self.dbprint('< relation()')
        self.debugIdent -= 1
        return

    def expression(self):
        self.debugIdent += 1
        self.dbprint('> expression()')

        if self.testarClasse('+','-'):
            self.sign('+', '-')

        self.term()

        if self.testarClasse('+', '-'):
            self.validarClasse('+', '-')
            self.term()

        self.debugIdent -= 1
        self.dbprint('< expression()')
        

    def sign(self):
        self.validarClasse('ADD', 'SUB')


    def term(self):
        self.debugIdent += 1
        self.dbprint('> term()')

        self.factor()

        if self.testarClasse('/', '*'):
            self.factors()

        self.debugIdent -= 1
        self.dbprint('< term()')


    def factor(self):
        self.debugIdent += 1
        self.dbprint('> factor()')

        if self.testarClasse(TokenClass.IDENTIFIER):
            self.validarClasse(TokenClass.IDENTIFIER)

        elif self.testarClasse(TokenClass.NUMBER):
            self.validarClasse(TokenClass.NUMBER)            

        elif self.testarClasse('('):
            self.validarClasse('(')
            self.expression()
            self.validarClasse(')')
        
        self.debugIdent <= 1
        self.dbprint('< factor()')
            

    def factors(self):
        self.debugIdent += 1
        self.dbprint('> factors()')

        self.validarClasse('/', '*')
        self.factor()

        self.debugIdent -= 1
        self.dbprint('< factors()')