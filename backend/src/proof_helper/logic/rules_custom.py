from proof_helper.core.proof import Proof, Step, Statement
from typing import List

class CustomRule:
    def __init__(self, name: str, proof: Proof):
        self.name = name
        self.proof = proof # Proof must be validated before construction
        self.conclusions = proof.conclusions
        self.premises = proof.premises

    def __call__(self, supports: List[Step], statement: Statement) -> bool:
        # Must have same number of supports as statements
        if len(supports) != len(self.premises):
            return False

        # All supports must be statements
        if not all(isinstance(s, Statement) for s in supports):
            return False

        # Match premise formulas
        given_formulas = {s.formula for s in supports}
        expected_formulas = {p.formula for p in self.premises}

        if given_formulas != expected_formulas:
            return False

        # Statement formula must match one of the rule's conclusions
        return any(statement.formula == c.formula for c in self.conclusions)

