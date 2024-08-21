from lex import Lex
from token import TokenClass


class Parser:
    def __init__(self, codigoFonte: str, ):
        self.codigoFonte = Lex(codigoFonte).code2tokens()       # uma lista com todas as palavras do código já classificadas
        self.atualToken = None                                  #
        self.debugIdent = 0                                     #


    def dbprint(self, msg: str):
        print(self.debugIdent * ' ' + msg)


    def proximoToken(self):
        self.atualToken = self.codigoFonte.pop(0)
        # print((1+self.debugIdent) * ' ' + 'CurrentToken:', self.atualToken)

    
    def analisar(self):
        self.dbprint('> analisar()')
        
        self.proximoToken()
        
        self.block()

        self.dbprint('< analisar()')

        if self.atualToken.token_class == TokenClass.EOF:
            return
        
        
    
    def block(self):
        self.debugIdent += 1
        self.dbprint('> block()')
        
        if self.atualToken is None:
            return

        if self.testarClasse(TokenClass.KEYWORD_CONST):
            self.constants()
        if self.testarClasse(TokenClass.KEYWORD_VAR):
            self.variables()
        if self.testarClasse(TokenClass.KEYWORD_PROCEDURE):
            self.procedures()
        if self.testarClasse(TokenClass.IDENTIFIER, TokenClass.KEYWORD_CALL, TokenClass.KEYWORD_BEGIN, TokenClass.KEYWORD_IF, TokenClass.KEYWORD_WHILE, TokenClass.KEYWORD_PRINT):
            self.statement()
        
        self.dbprint('< block()')
        self.debugIdent -= 1


    def constants(self):
        self.debugIdent += 1
        self.dbprint('> constants()')

        self.validarClasse(TokenClass.KEYWORD_CONST)
        self.constdecl()
        self.validarClasse(TokenClass.DELIM_SEMICOLON)

        self.dbprint('< constant()')
        self.debugIdent -= 1

    
    def variables(self):
        self.debugIdent += 1
        self.dbprint('> variables()')

        self.validarClasse(TokenClass.KEYWORD_VAR)
        self.vardecl()
        self.validarClasse(TokenClass.DELIM_SEMICOLON)
        
        self.dbprint('< variables()')
        self.debugIdent -= 1


    def procedures(self):
        self.debugIdent += 1
        self.dbprint('> procedures()')

        self.procdecl()
        if self.testarClasse(TokenClass.KEYWORD_PROCEDURE):
            self.procedures()
            
        self.dbprint('< procedures()')
        self.debugIdent -= 1


    def statement(self):
        self.debugIdent += 1
        self.dbprint('> statement()')

        if self.testarClasse(TokenClass.IDENTIFIER):
            self.validarClasse(TokenClass.IDENTIFIER)
            self.validarClasse(TokenClass.OPERATOR_ASSIGN)
            self.expression()

        elif self.testarClasse(TokenClass.KEYWORD_CALL):
            self.validarClasse(TokenClass.KEYWORD_CALL)
            self.validarClasse(TokenClass.IDENTIFIER)

        elif self.testarClasse(TokenClass.KEYWORD_BEGIN):
            self.validarClasse(TokenClass.KEYWORD_BEGIN)
            if self.testarClasse(TokenClass.IDENTIFIER, TokenClass.KEYWORD_CALL, TokenClass.KEYWORD_BEGIN, TokenClass.KEYWORD_IF, TokenClass.KEYWORD_WHILE, TokenClass.KEYWORD_PRINT):
                self.compound_stmt()
            self.validarClasse(TokenClass.KEYWORD_END)

        elif self.testarClasse(TokenClass.KEYWORD_IF):
            self.validarClasse(TokenClass.KEYWORD_IF)
            self.condition()
            self.validarClasse(TokenClass.KEYWORD_THEN)
            self.statement()

        elif self.testarClasse(TokenClass.KEYWORD_WHILE):
            self.validarClasse(TokenClass.KEYWORD_WHILE)
            self.condition()
            self.validarClasse(TokenClass.KEYWORD_DO)
            self.statement()

        elif self.testarClasse(TokenClass.KEYWORD_PRINT):
            self.validarClasse(TokenClass.KEYWORD_PRINT)
            self.expression()
            
        self.dbprint('< statement()')
        self.debugIdent -= 1


    def compound_stmt(self):
        self.statement()
        self.validarClasse(TokenClass.DELIM_SEMICOLON)
        if self.testarClasse(TokenClass.IDENTIFIER, TokenClass.KEYWORD_CALL, TokenClass.KEYWORD_BEGIN, TokenClass.KEYWORD_IF, TokenClass.KEYWORD_WHILE, TokenClass.KEYWORD_PRINT):
            # self.validarClasse(TokenClass.IDENTIFIER, TokenClass.KEYWORD_CALL, TokenClass.KEYWORD_BEGIN, TokenClass.KEYWORD_IF, TokenClass.KEYWORD_WHILE, TokenClass.KEYWORD_PRINT):
            self.compound_stmt()


    def constdecl(self):
        
        self.debugIdent += 1
        self.dbprint('> constdecl()')
        self.constdef()
        if self.testarClasse(TokenClass.DELIM_COMMA):
            self.validarClasse(TokenClass.DELIM_COMMA)
            self.constdecl()
            
        self.dbprint('< constdecl()')
        self.debugIdent -= 1


    def vardecl(self):
        self.debugIdent += 1
        self.dbprint('> vardecl()')
        
        self.validarClasse(TokenClass.IDENTIFIER)
        if self.testarClasse(TokenClass.DELIM_COMMA):
            self.validarClasse(TokenClass.DELIM_COMMA)
            self.vardecl()
            
        self.dbprint('< vardecl()')
        self.debugIdent -= 1


    def procdecl(self):
        self.debugIdent += 1
        self.dbprint('> procdecl()')

        self.validarClasse(TokenClass.KEYWORD_PROCEDURE)
        self.validarClasse(TokenClass.IDENTIFIER)
        self.validarClasse(TokenClass.DELIM_SEMICOLON)
        self.block()
        self.validarClasse(TokenClass.DELIM_SEMICOLON)

        self.dbprint('< procdecl()')
        self.debugIdent -= 1
        

    
    def constdef(self):
        self.debugIdent += 1
        self.dbprint('> constdef()')

        self.validarClasse(TokenClass.IDENTIFIER)
        self.validarClasse(TokenClass.RELATION_EQUAL)
        self.validarClasse(TokenClass.NUMBER)

        self.dbprint('< constdef()')
        self.debugIdent -= 1
        

    def condition(self):
        self.debugIdent += 1
        self.dbprint('> condition()')

        if self.testarClasse(TokenClass.KEYWORD_ODD):
            self.expression()
        elif self.testarClasse(TokenClass.KEYWORD_EVEN):
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

        if self.testarClasse(TokenClass.RELATION_EQUAL,TokenClass.RELATION_NOT_EQUAL,TokenClass.RELATION_LT,TokenClass.RELATION_LTE,TokenClass.RELATION_GT,TokenClass.RELATION_GTE, TokenClass.RELATION_ISDIV):
            self.validarClasse(TokenClass.RELATION_EQUAL,TokenClass.RELATION_NOT_EQUAL,TokenClass.RELATION_LT,TokenClass.RELATION_LTE,TokenClass.RELATION_GT,TokenClass.RELATION_GTE, TokenClass.RELATION_ISDIV)

            self.dbprint('< relation()')
            self.debugIdent -= 1
            return
        else:
            self.validarClasse(TokenClass.RELATION_EQUAL,TokenClass.RELATION_NOT_EQUAL,TokenClass.RELATION_LT,TokenClass.RELATION_LTE,TokenClass.RELATION_GT,TokenClass.RELATION_GTE, TokenClass.RELATION_ISDIV)
        

    def expression(self):
        self.debugIdent += 1
        self.dbprint('> expression()')

        if self.testarClasse(TokenClass.OPERATOR_ADD, TokenClass.OPERATOR_SUB):
            self.validarClasse(TokenClass.OPERATOR_ADD, TokenClass.OPERATOR_SUB)

        self.term()

        if self.testarClasse(TokenClass.OPERATOR_ADD, TokenClass.OPERATOR_SUB):
            self.validarClasse(TokenClass.OPERATOR_ADD, TokenClass.OPERATOR_SUB)
            self.term()

        self.debugIdent -= 1
        self.dbprint('< expression()')

    def term(self):
        self.debugIdent += 1
        self.dbprint('> term()')

        self.factor()

        if self.testarClasse(TokenClass.OPERATOR_DIV, TokenClass.OPERATOR_MUL):
            self.factors()

        self.debugIdent -= 1
        self.dbprint('< term()')


    def factor(self):
        self.debugIdent += 1
        self.dbprint('> factor()')

        if self.testarClasse(TokenClass.IDENTIFIER, TokenClass.NUMBER):
            self.validarClasse(TokenClass.IDENTIFIER, TokenClass.NUMBER)

        elif self.testarClasse(TokenClass.DELIM_OPEN_PAREN):
            self.validarClasse(TokenClass.DELIM_OPEN_PAREN)
            self.expression()
            self.validarClasse(TokenClass.DELIM_CLOSE_PAREN)
        
        self.debugIdent <= 1
        self.dbprint('< factor()')
            

    def factors(self):
        self.debugIdent += 1
        self.dbprint('> factors()')

        self.validarClasse(TokenClass.OPERATOR_DIV, TokenClass.OPERATOR_MUL)
        self.factor()

        self.debugIdent -= 1
        self.dbprint('< factors()')
        

    def testarClasse(self, *token_classes):
        """
            Testa se a classe do token atual é uma das classes em '*token_classes'.
        """

        print(self.debugIdent * ' ' + f'? testando classes {token_classes} => {self.atualToken}')
        
        # print('testar', self.atualToken)
        if self.atualToken is None:
            return False

        result = self.atualToken.token_class in token_classes
        
        # if(result):
        #     self.proximoToken()
        
        return result

    
    def validarClasse(self, *token_classes):

        print(self.debugIdent * ' ' + f'! validando classes {token_classes} => {self.atualToken}')
        
        # print('validar', self.atualToken)
        if self.atualToken is None:
            raise SyntaxError('Unexpected end of input.')

        if self.atualToken.token_class in token_classes:
            self.proximoToken()
        else:
            raise SyntaxError('Unexpected token {}. Expected one of: {}'.format(self.atualToken.token_class, token_classes))