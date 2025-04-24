from proof_helper.core.formula import *

import re

class FormulaParser:
    def __init__(self, src: str):
        self.tokens = self.tokenize(src)
        self.pos = 0

    def tokenize(self, src: str) -> list[str]:
        token_spec = r'¬|→|∧|∨|↔|⊥|\(|\)|[A-Za-z][A-Za-z0-9_]*'
        matches = list(re.finditer(token_spec, src))

        covered = [False] * len(src)

        for match in matches:
            for i in range(match.start(), match.end()):
                covered[i] = True

        for i, char in enumerate(src):
            if not covered[i] and not char.isspace():
                raise SyntaxError(f"Invalid character in formula: '{char}' at position {i}")

        return [m.group() for m in matches]

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self):
        self.pos += 1

    def eat(self, expected):
        if self.current() == expected:
            self.advance()
        else:
            raise SyntaxError(f"Expected '{expected}', found '{self.current()}'")

    def parse(self) -> Formula:
        return self.parse_iff()

    def parse_iff(self) -> Formula:
        left = self.parse_implies()
        while self.current() == '↔':
            self.advance()
            right = self.parse_implies()
            left = Iff(left, right)
        return left

    def parse_implies(self) -> Formula:
        left = self.parse_or()
        while self.current() == '→':
            self.advance()
            right = self.parse_or()
            left = Implies(left, right)
        return left

    def parse_or(self) -> Formula:
        left = self.parse_and()
        while self.current() == '∨':
            self.advance()
            right = self.parse_and()
            left = Or(left, right)
        return left

    def parse_and(self) -> Formula:
        left = self.parse_not()
        while self.current() == '∧':
            self.advance()
            right = self.parse_not()
            left = And(left, right)
        return left

    def parse_not(self) -> Formula:
        if self.current() == '¬':
            self.advance()
            return Not(self.parse_not())
        return self.parse_atom()

    def parse_atom(self) -> Formula:
        tok = self.current()
        if tok is None:
            raise SyntaxError("Unexpected end of input")
        if tok == '⊥':
            self.advance()
            return Bottom()
        if tok == '(':
            self.advance()
            expr = self.parse()
            self.eat(')')
            return expr
        if re.match(r'^[A-Za-z]', tok):
            self.advance()
            return Variable(tok)
        raise SyntaxError(f"Unexpected token: {tok}")

def parse_formula(src: str) -> Formula:
    return FormulaParser(src).parse()