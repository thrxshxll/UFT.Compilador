from enum import Enum


class TokenClass(Enum):
    KEYWORD = 1,
    RELATIONAL_OPERATOR = 2,
    OPERATOR = 3,
    ASSIGN_OPERATOR = 4,
    DELIM_OPEN_PAREN = 27,
    DELIM_CLOSE_PAREN = 28,
    DELIM_COMMA = 29,
    DELIM_SEMICOLON = 30,
    IDENTIFIER = 31,
    NUMBER= 32,
    COMMENT = 33,
    EOF = 34
    

class Token:
    def __init__(self, token_class: TokenClass, token_value):
        self.token_class = token_class
        self.token_value = token_value
    def __str__(self) -> str:
        return f'<Token class: {self.token_class}, value: {self.token_value}>'
