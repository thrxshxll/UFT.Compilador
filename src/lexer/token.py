from enum import Enum


class TokenClass(Enum):
    KEYWORD = 1,
    RELATIONAL_OPERATOR = 2,
    OPERATOR = 3,
    ASSIGN_OPERATOR = 4,
    DELIM_OPEN_PAREN = 5,
    DELIM_CLOSE_PAREN = 6,
    DELIM_COMMA = 7,
    DELIM_SEMICOLON = 8,
    IDENTIFIER = 9,
    NUMBER= 10,
    COMMENT = 11,
    EOF = 12
    

class Token:
    def __init__(self, token_class: TokenClass, token_value):
        self.token_class = token_class
        self.token_value = token_value
    def __str__(self) -> str:
        return f'<Token class: {self.token_class}, value: {self.token_value}>'
