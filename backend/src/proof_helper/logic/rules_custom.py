from proof_helper.core.proof import Proof, Step, Statement
from proof_helper.core.formula import Formula
from proof_helper.logic.rules_base import Rule
from typing import List, Optional

class CustomRule(Rule):
    def __init__(self, name: str, proof: Proof):
        self._name = name
        self.proof = proof  # Assumes proof is already validated
        self.premises = proof.premises
        self.conclusions = proof.conclusions

    def name(self) -> str:
        return self._name

    def num_supports(self) -> Optional[int]:
        return len(self.premises)

    def is_applicable(self, supports: List[Step]) -> bool:
        if len(supports) != len(self.premises):
            return False
        return all(isinstance(s, Statement) for s in supports)

    def verify(self, supports: List[Step], statement: Statement) -> bool:
        if not self.is_applicable(supports):
            return False

        given_formulas = {s.formula for s in supports}
        expected_formulas = {p.formula for p in self.premises}

        if given_formulas != expected_formulas:
            return False

        return any(statement.formula == c.formula for c in self.conclusions)
    
    def conclude(self, supports: list[Step]) -> list[Formula]:
        if not self.is_applicable(supports):
            return []
        return [c.formula for c in self.conclusions]