import re
from token import Token, TokenClass


class RuleInterface:
    def regex_rules(self) -> list[str]:
        pass
    def extract_token(self, match: str) -> Token:
        pass
    def check_match(self, content: str) -> re.Match:
        for rule in self.regex_rules():
            match = re.match(rule, content)
            if match:
                return match
        return None


class KeywordConst(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\bCONST\\b']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.KEYWORD_CONST, match)

class KeywordVar(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\bVAR\\b']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.KEYWORD_VAR, match)

class KeywordProcedure(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\bPROCEDURE\\b']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.KEYWORD_PROCEDURE, match)

class KeywordCall(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\bCALL\\b']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.KEYWORD_CALL, match)

class KeywordBegin(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\bBEGIN\\b']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.KEYWORD_BEGIN, match)

class KeywordEnd(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\bEND\\b']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.KEYWORD_END, match)

class KeywordIf(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\bIF\\b']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.KEYWORD_IF, match)

class KeywordNot(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\bNOT\\b']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.KEYWORD_NOT, match)

class KeywordThen(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\bTHEN\\b']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.KEYWORD_THEN, match)

class KeywordWhile(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\bWHILE\\b']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.KEYWORD_WHILE, match)

class KeywordDo(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\bDO\\b']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.KEYWORD_DO, match)

class KeywordPrint(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\bPRINT\\b']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.KEYWORD_PRINT, match)

class KeywordOdd(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\bODD\\b']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.KEYWORD_ODD, match)

class KeywordEven(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\bEVEN\\b']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.KEYWORD_EVEN, match)


class RelationEqual(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\=']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.RELATION_EQUAL, match)

class RelationNotEqual(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\#']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.RELATION_NOT_EQUAL, match)

class RelationLt(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\<']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.RELATION_LT, match)

class RelationLte(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\<\\=']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.RELATION_LTE, match)

class RelationGt(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\>']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.RELATION_GT, match)

class RelationGte(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\>\\=']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.RELATION_GTE, match)

class RelationIsDiv(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\/\\?']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.RELATION_ISDIV, match)


class OperatorAdd(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\+']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.OPERATOR_ADD, match)

class OperatorSub(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\-']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.OPERATOR_SUB, match)

class OperatorMul(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\*']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.OPERATOR_MUL, match)

class OperatorDiv(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\/']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.OPERATOR_DIV, match)

class OperatorAssign(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\<\\-']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.OPERATOR_ASSIGN, match)


class DelimiterOpenParen(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\(']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.DELIM_OPEN_PAREN, match)

class DelimiterCloseParen(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\)']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.DELIM_CLOSE_PAREN, match)

class DelimiterComma(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\,']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.DELIM_COMMA, match)

class DelimiterSemiColon(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\;']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.DELIM_SEMICOLON, match)

class Identifier(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['[a-zA-Z_][a-zA-Z0-9_]*']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.IDENTIFIER, match)

class Number(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\b(?<![A-Za-z_."\'])\d+(?![A-Za-z_."\'])\\b']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.NUMBER, match)

class Comment(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\{']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.COMMENT, match)

class Eof(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\.']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.EOF, match)