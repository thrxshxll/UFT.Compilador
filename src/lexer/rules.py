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


class Keywords(RuleInterface):
    def regex_rules(self) -> list[str]:
        return [r'\b(CONST|VAR|PROCEDURE|CALL|BEGIN|RETURN|END|IF|NOT|THEN|WHILE|DO|PRINT|ODD|EVEN)\b']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.KEYWORD, match)


class RelationalOperators(RuleInterface):
    def regex_rules(self) -> list[str]:
        return [
                r'<=|>=|/\?|=|#|=|<|>']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.RELATIONAL_OPERATOR, match)


class Operators(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['(\\+|\\-|\\*|\\/)']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.OPERATOR, match)


class AssignOperator(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\<\\-']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.ASSIGN_OPERATOR, match)


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

class EOF(RuleInterface):
    def regex_rules(self) -> list[str]:
        return ['\\.']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.EOF, match)