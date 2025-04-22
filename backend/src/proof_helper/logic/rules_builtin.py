from functools import wraps
from typing import Callable, Dict, List, Set, Optional
from proof_helper.core.proof import Step, Statement, Subproof, Proof
from proof_helper.core.formula import Formula, And, Or, Not, Bottom, Implies, Iff
from proof_helper.logic.rules_custom import CustomRule
from proof_helper.logic.rules_base import Rule

class AssumptionRule(Rule):
    def name(self) -> str:
        return "Assumption"
    
    def num_supports(self) -> Optional[int]:
        return 0
    
    def is_applicable(self, supports: list[Step]) -> bool:
        return len(supports) == 0
    
    def verify(self, supports: List[Step], statement: Statement) -> bool:
        return self.is_applicable(supports)
        
class ReiterationRule(Rule):
    def name(self) -> str:
        return "Reiteration"

    def num_supports(self) -> Optional[int]:
        return 1

    def is_applicable(self, supports: list[Step]) -> bool:
        return len(supports) == 1 and isinstance(supports[0], Statement)

    def verify(self, supports: List[Step], statement: Statement) -> bool:
        if not self.is_applicable(supports):
            return False
        support = supports[0]
        return support.formula == statement.formula


class AndIntroductionRule(Rule):
    def name(self) -> str:
        return "∧ Introduction"

    def num_supports(self) -> Optional[int]:
        return None  # variable number of conjuncts allowed

    def is_applicable(self, supports: list[Step]) -> bool:
        # Must all be statements
        return all(isinstance(s, Statement) for s in supports)

    def verify(self, supports: List[Step], statement: Statement) -> bool:
        if not self.is_applicable(supports):
            return False

        def collect_conjuncts(formula: Formula) -> Set[Formula]:
            if isinstance(formula, And):
                return collect_conjuncts(formula.left) | collect_conjuncts(formula.right)
            return {formula}

        statement_conjuncts = collect_conjuncts(statement.formula)

        support_conjuncts: Set[Formula] = set()
        for support in supports:
            support_conjuncts |= collect_conjuncts(support.formula)

        return statement_conjuncts == support_conjuncts

class OrIntroductionRule(Rule):
    def name(self) -> str:
        return "∨ Introduction"

    def num_supports(self) -> Optional[int]:
        return 1

    def is_applicable(self, supports: list[Step]) -> bool:
        return len(supports) == 1 and isinstance(supports[0], Statement)

    def verify(self, supports: List[Step], statement: Statement) -> bool:
        if not self.is_applicable(supports):
            return False

        def collect_disjuncts(formula: Formula) -> Set[Formula]:
            if isinstance(formula, Or):
                return collect_disjuncts(formula.left) | collect_disjuncts(formula.right)
            return {formula}

        disjuncts = collect_disjuncts(statement.formula)
        return supports[0].formula in disjuncts
class NotIntroductionRule(Rule):
    def name(self) -> str:
        return "¬ Introduction"

    def num_supports(self) -> Optional[int]:
        return 1

    def is_applicable(self, supports: list[Step]) -> bool:
        return (
            len(supports) == 1 and
            isinstance(supports[0], Subproof)
        )

    def verify(self, supports: List[Step], statement: Statement) -> bool:
        if not self.is_applicable(supports):
            return False

        support = supports[0]
        if not isinstance(statement.formula, Not):
            return False

        if support.assumption.formula != statement.formula.value:
            return False

        for step in support.steps:
            if isinstance(step, Statement) and isinstance(step.formula, Bottom):
                return True

        return False
    
class BottomIntroductionRule(Rule):
    def name(self) -> str:
        return "⊥ Introduction"

    def num_supports(self) -> Optional[int]:
        return 2

    def is_applicable(self, supports: list[Step]) -> bool:
        if len(supports) != 2:
            return False
        return all(isinstance(s, Statement) for s in supports)

    def verify(self, supports: List[Step], statement: Statement) -> bool:
        if not self.is_applicable(supports):
            return False

        a, b = supports
        formulas_match = (
            Not(a.formula) == b.formula or
            Not(b.formula) == a.formula
        )

        return formulas_match and isinstance(statement.formula, Bottom)

class ConditionalIntroductionRule(Rule):
    def name(self) -> str:
        return "→ Introduction"

    def num_supports(self) -> Optional[int]:
        return 1

    def is_applicable(self, supports: list[Step]) -> bool:
        return (
            len(supports) == 1 and
            isinstance(supports[0], Subproof) and
            bool(supports[0].steps)
        )

    def verify(self, supports: List[Step], statement: Statement) -> bool:
        if not self.is_applicable(supports):
            return False

        support = supports[0]
        assumption = support.assumption.formula
        last_step = support.steps[-1]
        if not isinstance(last_step, Statement):
            return False

        return statement.formula == Implies(assumption, last_step.formula)

class BiconditionalIntroductionRule(Rule):
    def name(self) -> str:
        return "↔ Introduction"

    def num_supports(self) -> Optional[int]:
        return 2

    def is_applicable(self, supports: list[Step]) -> bool:
        if len(supports) != 2:
            return False
        if not all(isinstance(s, Subproof) for s in supports):
            return False
        if not all(s.steps and isinstance(s.steps[-1], Statement) for s in supports):
            return False
        return True

    def verify(self, supports: List[Step], statement: Statement) -> bool:
        if not self.is_applicable(supports):
            return False

        a, b = supports
        a_assume, a_conclude = a.assumption.formula, a.steps[-1].formula
        b_assume, b_conclude = b.assumption.formula, b.steps[-1].formula

        expected1 = Iff(a_assume, a_conclude)
        expected2 = Iff(b_conclude, b_assume)

        return statement.formula == expected1 or statement.formula == expected2
class AndEliminationRule(Rule):
    def name(self) -> str:
        return "∧ Elimination"

    def num_supports(self) -> Optional[int]:
        return 1

    def is_applicable(self, supports: list[Step]) -> bool:
        return (
            len(supports) == 1 and
            isinstance(supports[0], Statement) and
            isinstance(supports[0].formula, And)
        )

    def verify(self, supports: list[Step], statement: Statement) -> bool:
        if not self.is_applicable(supports):
            return False

        def collect_conjuncts(formula: Formula) -> Set[Formula]:
            if isinstance(formula, And):
                return collect_conjuncts(formula.left) | collect_conjuncts(formula.right)
            return {formula}

        support_conjuncts = collect_conjuncts(supports[0].formula)
        stmt_conjuncts = collect_conjuncts(statement.formula)
        return stmt_conjuncts <= support_conjuncts

class OrEliminationRule(Rule):
    def name(self) -> str:
        return "∨ Elimination"

    def num_supports(self) -> Optional[int]:
        return None  # variable number of subproofs

    def is_applicable(self, supports: list[Step]) -> bool:
        if len(supports) < 2:
            return False
        if not isinstance(supports[0], Statement):
            return False
        if not all(isinstance(s, Subproof) for s in supports[1:]):
            return False
        return True

    def verify(self, supports: list[Step], statement: Statement) -> bool:
        if not self.is_applicable(supports):
            return False

        disj = supports[0]
        subproofs = supports[1:]

        def collect_disjuncts(formula: Formula) -> list[Formula]:
            if isinstance(formula, Or):
                return collect_disjuncts(formula.left) + collect_disjuncts(formula.right)
            return [formula]

        disjuncts = collect_disjuncts(disj.formula)
        if len(disjuncts) != len(subproofs):
            return False

        matched = set()
        conclusion = None

        for sp in subproofs:
            if not sp.steps or not isinstance(sp.steps[-1], Statement):
                return False
            assumption = sp.assumption.formula
            last = sp.steps[-1].formula

            if conclusion is None:
                conclusion = last
            elif last != conclusion:
                return False

            if assumption not in disjuncts or assumption in matched:
                return False
            matched.add(assumption)

        return conclusion == statement.formula and len(matched) == len(disjuncts)

class NotEliminationRule(Rule):
    def name(self) -> str:
        return "¬ Elimination"

    def num_supports(self) -> Optional[int]:
        return 1

    def is_applicable(self, supports: list[Step]) -> bool:
        return (
            len(supports) == 1 and
            isinstance(supports[0], Statement) and
            isinstance(supports[0].formula, Not) and
            isinstance(supports[0].formula.value, Not)
        )

    def verify(self, supports: list[Step], statement: Statement) -> bool:
        if not self.is_applicable(supports):
            return False
        return supports[0].formula.value.value == statement.formula

class BottomEliminationRule(Rule):
    def name(self) -> str:
        return "⊥ Elimination"

    def num_supports(self) -> Optional[int]:
        return 1

    def is_applicable(self, supports: list[Step]) -> bool:
        return (
            len(supports) == 1 and
            isinstance(supports[0], Statement) and
            isinstance(supports[0].formula, Bottom)
        )

    def verify(self, supports: list[Step], statement: Statement) -> bool:
        return self.is_applicable(supports)

class ConditionalEliminationRule(Rule):
    def name(self) -> str:
        return "→ Elimination"

    def num_supports(self) -> Optional[int]:
        return 2

    def is_applicable(self, supports: list[Step]) -> bool:
        return (
            len(supports) == 2 and
            all(isinstance(s, Statement) for s in supports)
        )

    def verify(self, supports: list[Step], statement: Statement) -> bool:
        if not self.is_applicable(supports):
            return False
        a, b = supports

        if not isinstance(a, Statement) or not isinstance(b, Statement):
            return False

        if isinstance(a.formula, Implies) and a.formula.left == b.formula:
            return statement.formula == a.formula.right
        if isinstance(b.formula, Implies) and b.formula.left == a.formula:
            return statement.formula == b.formula.right

        return False


class BiconditionalEliminationRule(Rule):
    def name(self) -> str:
        return "↔ Elimination"

    def num_supports(self) -> Optional[int]:
        return 2

    def is_applicable(self, supports: list[Step]) -> bool:
        return (
            len(supports) == 2 and
            all(isinstance(s, Statement) for s in supports)
        )

    def verify(self, supports: list[Step], statement: Statement) -> bool:
        if not self.is_applicable(supports):
            return False
        a, b = supports

        if not isinstance(a, Statement) or not isinstance(b, Statement):
            return False

        if isinstance(a.formula, Iff):
            if a.formula.left == b.formula:
                return statement.formula == a.formula.right
            if a.formula.right == b.formula:
                return statement.formula == a.formula.left

        if isinstance(b.formula, Iff):
            if b.formula.left == a.formula:
                return statement.formula == b.formula.right
            if b.formula.right == a.formula:
                return statement.formula == b.formula.left

        return False

BUILTIN_RULES: list[Rule] = [
    AssumptionRule(),
    ReiterationRule(),
    AndIntroductionRule(),
    AndEliminationRule(),
    OrIntroductionRule(),
    OrEliminationRule(),
    NotIntroductionRule(),
    NotEliminationRule(),
    BottomIntroductionRule(),
    BottomEliminationRule(),
    ConditionalIntroductionRule(),
    ConditionalEliminationRule(),
    BiconditionalIntroductionRule(),
    BiconditionalEliminationRule(),
]