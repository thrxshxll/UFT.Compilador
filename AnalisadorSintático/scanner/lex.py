from token import Token
import rules
import re


class Lex:
    def __init__(self, content: str):
        self.rules = [ \
            rules.KeywordRule(), \
            rules.CommentRule(), \
            rules.OperatorRule(), \
            rules.DelimiterRule(), \
            rules.IntConstantRule(), \
            rules.IdRule() ]
        self.content = content


    def next(self) -> Token:
        if not self.content:
            return None
            
        for rule in self.rules:
            match = rule.check_match(self.content)
            if(match):
                if match.group() == '{':
                    self.content = self.content[re.search('}', self.content).end():]
                # else:
                    # print(f'matching rule {rule.__class__.__name__}: {match}') # DEBUG
            else:
                continue
            
            endpos = match.end()
            self.content = self.content[endpos:].lstrip()
            return rule.extract_token(match.group(0))

        raise Exception(f'Lexical Error: symbol {self.content[0]} not recognized')
