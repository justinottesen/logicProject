from proof_helper.core.proof import Proof, Step, Statement
from proof_helper.core.formula import Formula
from proof_helper.logic.rules_base import Rule
from typing import List, Optional
from itertools import permutations

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
        
        # Special case: no-premise rule (supports must be empty)
        if not self.premises and not supports:
            return any(statement.formula.match(c.formula, {}) for c in self.conclusions)

        # Try all permutations of supports matched to premises
        for perm in permutations(supports, len(self.premises)):
            subst: dict[str, Formula] = {}
            if all(prem.formula.match(sup.formula, subst) for prem, sup in zip(self.premises, perm)):
                for concl in self.conclusions:
                    if concl.formula.substitute(subst) == statement.formula:
                        return True
        return False
    
    def conclude(self, supports: list[Step]) -> list[Formula]:
        if not self.is_applicable(supports):
            return []
        
        # Special case: no-premise rule (supports must be empty)
        if not self.premises and not supports:
            return [c.formula for c in self.conclusions]

        for perm in permutations(supports, len(self.premises)):
            subst: dict[str, Formula] = {}
            if all(prem.formula.match(sup.formula, subst) for prem, sup in zip(self.premises, perm)):
                return [concl.formula.substitute(subst) for concl in self.conclusions]
        return []
