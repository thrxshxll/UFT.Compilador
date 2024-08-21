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


class KeywordRule(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\b(var|begin|end|while|do|ret|VAR|CONST|PROCEDURE|BEGIN|END|WHILE|DO|IF|THEN|CALL|PRINT|ODD|EVEN)\\b']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.KEYWORD, match)


class OperatorRule(RuleInterface):
    def regex_rules(self) -> list[str]:
        #   Operadores 
        return ['\\<\\=|\\>\\=|\\<\\-|\\/\\?|\\#|\\<|\\>|\\=|\\+|\\*|\\/']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.OPERATOR, match)


class DelimiterRule(RuleInterface):
    def regex_rules(self) -> list[str]:
        #   Delimitadores
        return ['\\(|\\)|\\;|\\.|\\,']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.DELIMITER, match)


class IntConstantRule(RuleInterface):
    def regex_rules(self) -> list[str]:
        # int
        return ['\\b(?<![A-Za-z_."\'])\d+(?![A-Za-z_."\'])\\b']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.INT_CONSTANT, int(match))


class IdRule(RuleInterface):
    def regex_rules(self) -> list[str]:
        #   nome de variável, função, struct
        return ['[a-zA-Z_][a-zA-Z0-9_]*']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.ID, match)


class CommentRule(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\{']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.COMMENT, match)