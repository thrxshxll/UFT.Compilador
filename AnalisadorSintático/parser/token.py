from enum import Enum


class TokenClass(Enum):
    KEYWORD_CONST = 1,
    KEYWORD_VAR = 2,
    KEYWORD_PROCEDURE = 3,
    KEYWORD_CALL = 4,
    KEYWORD_BEGIN = 5,
    KEYWORD_END = 6,
    KEYWORD_IF = 7,
    KEYWORD_NOT = 8,
    KEYWORD_THEN = 9,
    KEYWORD_WHILE = 10,
    KEYWORD_DO = 11,
    KEYWORD_PRINT = 12,
    KEYWORD_ODD = 13,
    KEYWORD_EVEN = 14,
    RELATION_EQUAL = 15,
    RELATION_NOT_EQUAL = 16,
    RELATION_LT = 17,
    RELATION_LTE = 18,
    RELATION_GT = 19,
    RELATION_GTE = 20,
    RELATION_ISDIV = 21,
    OPERATOR_ADD = 22,
    OPERATOR_SUB = 23,
    OPERATOR_MUL = 24,
    OPERATOR_DIV = 25,
    OPERATOR_ASSIGN = 26,
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
