from token import Token
import rules
import re


class Lex:
    def __init__(self, content: str, rules: list[rules.RuleInterface]):
        self.rules = rules
        self.content = content


    def next(self) -> Token:
        if not self.content:
            return None
        
        for rule in self.rules:
            match = rule.check_match(self.content)
            if(match):
                if match.group() == '//':
                    self.content = self.content[re.match('.*', self.content).end()-1:]
                if match.group() == '/*':
                    self.content = self.content[re.search('\*/', self.content).end():]
                    
                # print(f'matching rule {rule.__class__.__name__}: {match}') # DEBUG
            else:
                continue
            
            endpos = match.end()
            self.content = self.content[endpos:].lstrip()
            print(self.content)
            return rule.extract_token(match.group(0))

        raise Exception(f'Lexical Error: symbol {self.content[0]} not recognized')
