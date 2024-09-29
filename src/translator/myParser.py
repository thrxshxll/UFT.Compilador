from lex import Lex
from token import TokenClass


class Parser:
    def __init__(self, codigoFonte: str, ):
        self.codigoFonte = Lex(codigoFonte).code2tokens()       # uma lista com todas as palavras do código já classificadas
        self.atualToken = None                                  #
        self.blockIdent = 0                                     # Auxilia nas indetações que devem ser feitas em def, if, while 


    def proximoToken(self):
        self.atualToken = self.codigoFonte.pop(0)
        # print((1+self.debugIdent) * ' ' + 'CurrentToken:', self.atualToken)

    
    def analisar(self):
        
        self.proximoToken()
        
        print(self.block())

        if self.atualToken.token_class == TokenClass.EOF:
            return
        
    def block(self):
    # <block> --> <constants>? <variables>? <procedures>? <statement>?
        
        if self.atualToken is None:
            return

        blockbuff = ''
        if self.testarClasse(TokenClass.KEYWORD_CONST):
            blockbuff += self.constants()
        if self.testarClasse(TokenClass.KEYWORD_VAR):
            blockbuff += self.variables()
        if self.testarClasse(TokenClass.KEYWORD_PROCEDURE):
            blockbuff += self.procedures()
        if self.testarClasse(TokenClass.IDENTIFIER, TokenClass.KEYWORD_CALL, TokenClass.KEYWORD_BEGIN, TokenClass.KEYWORD_IF, TokenClass.KEYWORD_WHILE, TokenClass.KEYWORD_PRINT):
            blockbuff += self.statement()
        
        return blockbuff


    def constants(self):
    # <constants> --> "CONST" <constdecl> ";"

        self.validarClasse(TokenClass.KEYWORD_CONST)
        constDecl = self.constdecl()
        self.validarClasse(TokenClass.DELIM_SEMICOLON)

        return self.blockIdent * ' ' + constDecl + '\n'

    
    def variables(self):
        # <vardecl> --> <Ident> "," <vardecl> | <Ident>

        self.validarClasse(TokenClass.KEYWORD_VAR)
        retornVardecl = self.vardecl()
        self.validarClasse(TokenClass.DELIM_SEMICOLON)
        
        return self.blockIdent * ' ' +retornVardecl + '\n'


    def procedures(self):
        # <procedures>         --> <procdecl> <procedures>?
        
        buffer = '\n' + self.procdecl() + '\n'
        if self.testarClasse(TokenClass.KEYWORD_PROCEDURE):
            buffer += self.procedures()

        return buffer


    def statement(self):
        # <statement> --> <Ident> "<-" <expression>
        #               | "CALL" <Ident>
        #               | "BEGIN" <compound statement> "END"
        #               | "IF" "NOT"? <condition> "THEN" <statement>
        #               | "WHILE" "NOT"? <condition> "DO" <statement>
        #               | "PRINT" <expression>

        if self.testarClasse(TokenClass.IDENTIFIER):
            id = self.validarClasse(TokenClass.IDENTIFIER)
            self.validarClasse(TokenClass.OPERATOR_ASSIGN)
            exp = self.expression()
            return f'{id} = {exp}\n'

        elif self.testarClasse(TokenClass.KEYWORD_CALL):
            self.validarClasse(TokenClass.KEYWORD_CALL)
            funcName = self.validarClasse(TokenClass.IDENTIFIER)
            return f'{funcName}()\n'

        elif self.testarClasse(TokenClass.KEYWORD_BEGIN):
            self.validarClasse(TokenClass.KEYWORD_BEGIN)
            # retornoCompStmt = ''
            if self.testarClasse(TokenClass.IDENTIFIER, TokenClass.KEYWORD_CALL, TokenClass.KEYWORD_BEGIN, TokenClass.KEYWORD_IF, TokenClass.KEYWORD_WHILE, TokenClass.KEYWORD_PRINT):
                retornoCompStmt = self.compound_stmt()
            self.validarClasse(TokenClass.KEYWORD_END)
            return retornoCompStmt

        elif self.testarClasse(TokenClass.KEYWORD_IF):
            self.validarClasse(TokenClass.KEYWORD_IF)
            self.blockIdent += 4
            retornoCondition = self.condition()
            self.validarClasse(TokenClass.KEYWORD_THEN)

            retornoStatement = ''
            if not self.testarClasse(TokenClass.KEYWORD_BEGIN):
                retornoStatement += self.blockIdent * ' '

            retornoStatement += self.statement()
            msg = f'if {retornoCondition}:\n{retornoStatement}'
            self.blockIdent -= 4
            return msg

        elif self.testarClasse(TokenClass.KEYWORD_WHILE):
            self.validarClasse(TokenClass.KEYWORD_WHILE)
            self.blockIdent += 4
            retornoCondition = self.condition()
            self.validarClasse(TokenClass.KEYWORD_DO)
            retornoStatement = self.statement()
            msg = f'while {retornoCondition}:\n{retornoStatement}'
            self.blockIdent -= 4
            return msg

        elif self.testarClasse(TokenClass.KEYWORD_PRINT):
            self.validarClasse(TokenClass.KEYWORD_PRINT)
            retornoExpression = self.expression()
            return f'print({retornoExpression})\n'


    def compound_stmt(self):
        # <compound statement> --> (<statement> ";")*
        
        buffer = self.statement()
        self.validarClasse(TokenClass.DELIM_SEMICOLON)
        if self.testarClasse(TokenClass.IDENTIFIER, TokenClass.KEYWORD_CALL, TokenClass.KEYWORD_BEGIN, TokenClass.KEYWORD_IF, TokenClass.KEYWORD_WHILE, TokenClass.KEYWORD_PRINT):
            buffer += self.compound_stmt()
        return self.blockIdent * ' ' + buffer


    def constdecl(self):
        # <constdecl> --> <constdef> "," <constdecl>
        #               | <constdef>
        
        constDef = self.constdef()
        if self.testarClasse(TokenClass.DELIM_COMMA):
            self.validarClasse(TokenClass.DELIM_COMMA)
            constDef += self.constdecl()
            
        return constDef


    def vardecl(self):
        # <vardecl> --> <Ident> "," <vardecl>
        #             | <Ident>
        
        id = self.validarClasse(TokenClass.IDENTIFIER) + ' = 0'
        if self.testarClasse(TokenClass.DELIM_COMMA):
            self.validarClasse(TokenClass.DELIM_COMMA)
            id += '\n' + self.vardecl()

        return id


    def procdecl(self):
        # <procdecl> --> "PROCEDURE" <Ident> ";" <block> ";"

        self.blockIdent += 4

        self.validarClasse(TokenClass.KEYWORD_PROCEDURE)
        id = self.validarClasse(TokenClass.IDENTIFIER)
        self.validarClasse(TokenClass.DELIM_SEMICOLON)
        block = self.block()
        self.validarClasse(TokenClass.DELIM_SEMICOLON)

        msg = f'def {id}():\n{block}'
        self.blockIdent -= 4
        return msg

    
    def constdef(self):
        # <constdef> --> <Ident> "=" <Number>

        id = self.validarClasse(TokenClass.IDENTIFIER)
        re = self.validarClasse(TokenClass.RELATION_EQUAL)
        nu = self.validarClasse(TokenClass.NUMBER)

        return f'{id} = {nu}'


    def condition(self):
        # <condition> --> "ODD" <expression>
        #               | "EVEN" <expression>
        #               | <expression> <relation> <expression>

        if self.testarClasse(TokenClass.KEYWORD_ODD):
            self.validarClasse(TokenClass.KEYWORD_ODD)
            exp = self.expression()
            return f'{exp} % 2 != 0'

        elif self.testarClasse(TokenClass.KEYWORD_EVEN):
            self.validarClasse(TokenClass.KEYWORD_EVEN)
            exp = self.expression()
            return f'{exp} % 2 == 0'

        else:
            exp1 = self.expression()
            rel = self.relation()
            exp2 = self.expression()

            if rel == '%':
                return f'{exp1} % {exp2} == 0'
            return f'{exp1} {rel} {exp2}'


    def relation(self):
        # <relation> --> "="
        #              | "#"
        #              | "<"
        #              | "<="
        #              | ">"
        #              | ">="
        #              | "/?"

        if self.testarClasse(TokenClass.RELATION_EQUAL,TokenClass.RELATION_NOT_EQUAL,TokenClass.RELATION_LT,TokenClass.RELATION_LTE,TokenClass.RELATION_GT,TokenClass.RELATION_GTE, TokenClass.RELATION_ISDIV):
            buffer = self.validarClasse(TokenClass.RELATION_EQUAL,TokenClass.RELATION_NOT_EQUAL,TokenClass.RELATION_LT,TokenClass.RELATION_LTE,TokenClass.RELATION_GT,TokenClass.RELATION_GTE, TokenClass.RELATION_ISDIV)

            if buffer == '/?':
                buffer = '%'

            return buffer
        else:
            self.validarClasse(TokenClass.RELATION_EQUAL,TokenClass.RELATION_NOT_EQUAL,TokenClass.RELATION_LT,TokenClass.RELATION_LTE,TokenClass.RELATION_GT,TokenClass.RELATION_GTE, TokenClass.RELATION_ISDIV)
        

    def expression(self):
        # <expression> --> <sign>? <term> <terms>?

        exp = ''
        if self.testarClasse(TokenClass.OPERATOR_ADD, TokenClass.OPERATOR_SUB):
            exp += self.validarClasse(TokenClass.OPERATOR_ADD, TokenClass.OPERATOR_SUB)

        exp += self.term()

        if self.testarClasse(TokenClass.OPERATOR_ADD, TokenClass.OPERATOR_SUB):
            exp += self.validarClasse(TokenClass.OPERATOR_ADD, TokenClass.OPERATOR_SUB)
            exp += self.term()

        return exp


    def term(self):
        # <terms> --> "+" <term>
        #           | "-" <term>

        buffer = self.factor()

        # <factors>?
        if self.testarClasse(TokenClass.OPERATOR_DIV, TokenClass.OPERATOR_MUL):
            buffer += self.factors()

        return buffer


    def factor(self):
        # <factor> --> <Ident>
        #            | <Number>
        #            | "(" <expression> ")"

        if self.testarClasse(TokenClass.IDENTIFIER, TokenClass.NUMBER):
            buffer = self.validarClasse(TokenClass.IDENTIFIER, TokenClass.NUMBER)

        elif self.testarClasse(TokenClass.DELIM_OPEN_PAREN):
            buffer = self.validarClasse(TokenClass.DELIM_OPEN_PAREN)
            buffer += self.expression()
            buffer += self.validarClasse(TokenClass.DELIM_CLOSE_PAREN)
        
        return buffer
            

    def factors(self):
        # <factors> -->   "/" <factor>
        #               | "*" <factor>

        buffer = self.validarClasse(TokenClass.OPERATOR_DIV, TokenClass.OPERATOR_MUL)
        buffer += self.factor()

        return buffer
        

    def testarClasse(self, *token_classes):
        """
            Testa se a classe do token atual é uma das classes em '*token_classes'.
        """

        # print(self.debugIdent * ' ' + f'? testando classes {token_classes} => {self.atualToken}')
        
        if self.atualToken is None:
            return False

        result = self.atualToken.token_class in token_classes
        
        return result

    
    def validarClasse(self, *token_classes):
        """
            Valida se a classe do token atual é uma das classes em '*token_classes';
            se for, pega o próximo token, se não, gera um erro de sintaxe.
        """

        # print(self.debugIdent * ' ' + f'! validando classes {token_classes} => {self.atualToken}')
        
        if self.atualToken is None:
            raise SyntaxError('Unexpected end of input.')

        if self.atualToken.token_class in token_classes:
            hold = self.atualToken.token_value
            self.proximoToken()
            return hold
        else:
            raise SyntaxError('Unexpected token {}. Expected one of: {}'.format(self.atualToken.token_class, token_classes))