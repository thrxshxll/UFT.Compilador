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

        if (self.atualToken.token_value in token_classes) or (self.atualToken.token_class in token_classes):
            self.proximoToken()
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
        self.dbprint('> program()')
        
        self.proximoToken()
        
        self.block()

        self.validarClasse(TokenClass.EOF)

        self.dbprint('< program()')
                
        
    def block(self):
        self.dbprint('> block()')
        self.debugIdent += 2
        
        if self.atualToken is None:
            return

        if self.testarClasse('CONST'):
            self.constants()
        if self.testarClasse('VAR'):
            self.variables()
        if self.testarClasse('PROCEDURE'):
            self.procedures()
        if self.testarClasse(TokenClass.IDENTIFIER,'CALL', 'BEGIN','IF','WHILE','PRINT'):
            self.statement()

        
        self.debugIdent -= 2
        self.dbprint('< block()')


    def constants(self):
        self.dbprint('> constants()')
        self.debugIdent += 2

        self.validarClasse('CONST')
        self.constdecl()
        self.validarClasse(';')

        self.debugIdent -= 2
        self.dbprint('< constant()')

    
    def variables(self):
        self.dbprint('> variables()')
        self.debugIdent += 2

        self.validarClasse('VAR')
        self.vardecl()
        self.validarClasse(';')
        
        self.debugIdent -= 2
        self.dbprint('< variables()')


    def procedures(self):
        self.dbprint('> procedures()')
        self.debugIdent += 2

        self.procdecl()
        if self.testarClasse('PROCEDURE'):
            self.procedures()
            
        self.debugIdent -= 2
        self.dbprint('< procedures()')


    def statement(self):
        self.dbprint('> statement()')
        self.debugIdent += 2

        if self.testarClasse(TokenClass.IDENTIFIER):
            self.validarClasse(TokenClass.IDENTIFIER)
            self.validarClasse('<-')
            self.expression()

        elif self.testarClasse('CALL'):
            self.validarClasse('CALL')
            self.validarClasse(TokenClass.IDENTIFIER)
            if self.testarClasse(TokenClass.IDENTIFIER, TokenClass.NUMBER):
                self.argdecl()

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

        
        elif self.testarClasse('RETURN'):
            self.validarClasse('RETURN')
            self.validarClasse(TokenClass.IDENTIFIER)


        elif self.testarClasse('BEGIN'):
            self.validarClasse('BEGIN')
            self.compound_stmt()
            self.validarClasse('END')
            
        self.debugIdent -= 2
        self.dbprint('< statement()')


    def compound_stmt(self):
        self.dbprint('> compound_stmt()')
        self.debugIdent += 2

        self.statement()
        self.validarClasse(';')
        if self.testarClasse(TokenClass.IDENTIFIER,'CALL', 'BEGIN','IF','WHILE','PRINT', 'RETURN'):
            self.compound_stmt()

        self.debugIdent -= 2
        self.dbprint('< compound_stmt()')


    def constdecl(self):
        
        self.dbprint('> constdecl()')
        self.debugIdent += 2
        if self.testarClasse(TokenClass.IDENTIFIER):
            self.constdef()
        if self.testarClasse(','):
            self.validarClasse(',')
            self.constdecl()
            
        self.debugIdent -= 2
        self.dbprint('< constdecl()')


    def vardecl(self):
        self.dbprint('> vardecl()')
        self.debugIdent += 2
        
        self.validarClasse(TokenClass.IDENTIFIER)
        if self.testarClasse(','):
            self.validarClasse(',')
            self.vardecl()
            
        self.debugIdent -= 2
        self.dbprint('< vardecl()')


    def argdecl(self):
        
        f'{self.validarClasse(TokenClass.IDENTIFIER)}'
        if self.testarClasse(','):
            self.validarClasse(',')
            self.argdecl()


    def procdecl(self):
        self.dbprint('> procdecl()')
        self.debugIdent += 2

        self.validarClasse('PROCEDURE')
        self.validarClasse(TokenClass.IDENTIFIER)
        if self.testarClasse(TokenClass.IDENTIFIER, TokenClass.NUMBER):
            self.argdecl()
        self.validarClasse(';')
        self.block()
        self.validarClasse(';')

        self.debugIdent -= 2
        self.dbprint('< procdecl()')
        
    
    def constdef(self):
        self.dbprint('> constdef()')
        self.debugIdent += 2

        self.validarClasse(TokenClass.IDENTIFIER)
        self.validarClasse('=')
        self.validarClasse(TokenClass.NUMBER)

        self.debugIdent -= 2
        self.dbprint('< constdef()')
        

    def condition(self):
        self.dbprint('> condition()')
        self.debugIdent += 2

        if self.testarClasse('ODD', 'EVEN'):
            self.validarClasse('ODD', 'EVEN')
            self.expression()
        else:
            self.expression()
            self.relation()
            self.expression()

        self.debugIdent -= 2
        self.dbprint('< condition()')


    def relation(self):
        self.dbprint('> relation()')
        self.debugIdent += 2

        self.validarClasse('=','#','<','<=','>','>=','/?')

        self.debugIdent -= 2
        self.dbprint('< relation()')
        return

    def expression(self):
        self.dbprint('> expression()')
        self.debugIdent += 2

        if self.testarClasse('+','-'):
            self.sign()

        self.term()

        if self.testarClasse('+', '-'):
            self.sign()
            self.term()

        self.debugIdent -= 2
        self.dbprint('< expression()')
        

    def sign(self):
        self.validarClasse('+', '-')


    def term(self):
        self.dbprint('> term()')
        self.debugIdent += 2

        self.factor()

        if self.testarClasse('/', '*'):
            self.factors()

        self.debugIdent -= 2
        self.dbprint('< term()')


    def factor(self):
        self.dbprint('> factor()')
        self.debugIdent += 2

        if self.testarClasse(TokenClass.IDENTIFIER):
            self.validarClasse(TokenClass.IDENTIFIER)

        elif self.testarClasse(TokenClass.NUMBER):
            self.validarClasse(TokenClass.NUMBER)            

        elif self.testarClasse('('):
            self.validarClasse('(')
            self.expression()
            self.validarClasse(')')
        
        self.debugIdent -= 2
        self.dbprint('< factor()')
            

    def factors(self):
        self.dbprint('> factors()')
        self.debugIdent += 2

        self.validarClasse('/', '*')
        self.factor()

        self.debugIdent -= 2
        self.dbprint('< factors()')