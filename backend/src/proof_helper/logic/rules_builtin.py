from functools import wraps
from typing import Callable, Dict, List, Set, Optional
from proof_helper.core.proof import Step, Statement, Subproof, Proof
from proof_helper.core.formula import Formula, And, Or, Not, Bottom, Implies, Iff, Variable
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
    
    def conclude(self, supports: list[Step]) -> list[Formula]:
        return []
        
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
    
    def conclude(self, supports: list[Step]) -> list[Formula]:
        if not self.is_applicable(supports):
            return []
        return [ s.formula for s in supports ]


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

    def conclude(self, supports: list[Step]) -> list[Formula]:
        if not self.is_applicable(supports):
            return []
        
        # Generate a single top-level conjunction, nesting left-to-right
        formulas = [s.formula for s in supports]
        if not formulas:
            return []

        result = formulas[0]
        for f in formulas[1:]:
            result = And(result, f)
        return [result]

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
    
    def conclude(self, supports: list[Step], goals: Optional[list[Formula]] = None) -> list[Formula]:
        if not self.is_applicable(supports):
            return []

        if not supports:
            return []

        support_formula = supports[0].formula

        # If no goals provided, default to generic disjunction
        if goals is None:
            return [Or(support_formula, support_formula)]

        suggested = []
        for goal in goals:
            def collect_disjuncts(f: Formula) -> list[Formula]:
                if isinstance(f, Or):
                    return collect_disjuncts(f.left) + collect_disjuncts(f.right)
                return [f]

            disjuncts = collect_disjuncts(goal)

            # If the support formula is already part of a disjunction, suggest the whole goal
            if support_formula in disjuncts:
                suggested.append(goal)
            else:
                # Suggest new Or with each disjunct in the goal
                suggested.extend([
                    Or(support_formula, d) for d in disjuncts if d != support_formula
                ])

        return suggested

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
    
    def conclude(self, supports: list[Step]) -> list[Formula]:
        if not self.is_applicable(supports):
            return []
        
        support = supports[0]
        return [Not(support.assumption.formula)]
    
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
    
    def conclude(self, supports: list[Step]) -> list[Formula]:
        if not self.is_applicable(supports):
            return []
        return [Bottom()]

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
    
    def conclude(self, supports: list[Step]) -> list[Formula]:
        print(supports)
        if not self.is_applicable(supports):
            return []
        sp = supports[0]
        return [Implies(sp.assumption.formula, sp.steps[-1].formula)]

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
    
    def conclude(self, supports: List[Step]) -> List[Formula]:
        if not self.is_applicable(supports):
            return []
        
        a, b = supports
        a_assume, a_conclude = a.assumption.formula, a.steps[-1].formula
        b_assume, b_conclude = b.assumption.formula, b.steps[-1].formula

        if a_assume == b_conclude and a_conclude == b_assume:
            return [Iff(a_assume, a_conclude)]
        elif a_assume == a_assume and a_conclude == b_conclude and b_assume == b_assume:
            return [Iff(a_assume, a_conclude)]
        else:
            return []

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
    
    def conclude(self, supports: List[Step]) -> List[Formula]:
        if not self.is_applicable(supports):
            return []
        formula = supports[0].formula
        def collect(f: Formula) -> List[Formula]:
            if isinstance(f, And):
                return collect(f.left) + collect(f.right)
            return [f]

        return collect(formula)


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
    
    def conclude(self, supports: List[Step]) -> List[Formula]:
        if not self.is_applicable(supports):
            return []
        
        disj = supports[0]
        subproofs = supports[1:]

        conclusions = [sp.steps[-1].formula for sp in subproofs]
        if all(c == conclusions[0] for c in conclusions):
            return [conclusions[0]]
        return []


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
    
    def conclude(self, supports: List[Step]) -> List[Formula]:
        if len(supports) != 1 or not isinstance(supports[0], Statement):
            return []
        formula = supports[0].formula
        if isinstance(formula, Not) and isinstance(formula.value, Not):
            return [formula.value.value]
        return []


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
    
    from proof_helper.core.formula import Bottom

    def conclude(self, supports: List[Step]) -> List[Formula]:
        return [] # This is used for generation, and anything can be concluded


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
    
    def conclude(self, supports: List[Step]) -> List[Formula]:
        if not self.is_applicable(supports):
            return []
        
        if len(supports) != 2:
            return []
        a, b = supports
        if not isinstance(a, Statement) or not isinstance(b, Statement):
            return []

        if isinstance(a.formula, Implies) and a.formula.left == b.formula:
            return [a.formula.right]
        if isinstance(b.formula, Implies) and b.formula.left == a.formula:
            return [b.formula.right]
        return []



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

    def conclude(self, supports: List[Step]) -> List[Formula]:
        if not self.is_applicable(supports):
            return []
        
        if len(supports) != 2:
            return []
        a, b = supports
        if not isinstance(a, Statement) or not isinstance(b, Statement):
            return []

        if isinstance(a.formula, Iff):
            if a.formula.left == b.formula:
                return [a.formula.right]
            if a.formula.right == b.formula:
                return [a.formula.left]
        if isinstance(b.formula, Iff):
            if b.formula.left == a.formula:
                return [b.formula.right]
            if b.formula.right == a.formula:
                return [b.formula.left]
        return []


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