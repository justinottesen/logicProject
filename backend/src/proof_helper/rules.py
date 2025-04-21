from functools import wraps
from typing import Callable, Dict, List, Set
from proof_helper.proof import Step, Statement, Subproof
from proof_helper.formula import Formula, And, Or, Not, Bottom, Implies, Iff

# Each rule takes premises + subproofs and returns a derived formula
RuleFn = Callable[[List[Step], Statement], bool]

class RuleChecker:
    def __init__(self):
        self.rules: Dict[str, RuleFn] = {
            # Assumption - For premises & subproof assumptions
            "Assumption": rule_wrapper(assumption_rule),
            # Introduction Rules
            "∧ Introduction": rule_wrapper(and_introduction_rule),
            "∨ Introduction": rule_wrapper(or_introduction_rule),
            "¬ Introduction": rule_wrapper(not_introduction_rule),
            "⊥ Introduction": rule_wrapper(bottom_introduction_rule),
            "→ Introduction": rule_wrapper(conditional_introduction_rule),
            "↔ Introduction": rule_wrapper(biconditional_introduction_rule),
        }

    def get(self, name: str) -> RuleFn:
        return self.rules[name]

    def has(self, name: str) -> bool:
        return name in self.rules
    
def rule_wrapper(fn: RuleFn) -> RuleFn:
    @wraps(fn)
    def wrapped(supports: List[Step], statement: Statement):
        # All statements must have rules
        if statement.rule is None:
            return False
        # Sanity check of type
        if not isinstance(statement, Statement):
            return False
        # Supporting steps must be before the statement
        for support in supports:
            if not support.id.is_before(statement.id):
                return False
        # Supporting steps must match statement premises
        if set(map(lambda x: x.id, supports)) != set(statement.premises):
            return False
        return fn(supports, statement)
    return wrapped

def assumption_rule(supports: List[Step], statement: Statement) -> bool:
    # Assumption does not require any supporting steps (premises & subproofs)
    return not supports and statement

def and_introduction_rule(supports: List[Step], statement: Statement) -> bool:
    def collect_conjuncts(formula: Formula) -> Set[Formula]:
        if isinstance(formula, And):
            return collect_conjuncts(formula.left) | collect_conjuncts(formula.right)
        else:
            return { formula }
    
    # Collect the top level conjunctions in the statement
    statement_conjuncts = collect_conjuncts(statement.formula)

    # All supporting steps...
    supporting_conjuncts: Set[Formula] = set()
    for support in supports:
        # Must be statements
        if not isinstance(support, Statement):
            return False
        supporting_conjuncts |= collect_conjuncts(support.formula)

    # Both sets of conjunctions must be subsets of each other
    return statement_conjuncts == supporting_conjuncts

def or_introduction_rule(supports: List[Step], statement: Statement) -> bool:
    def collect_disjuncts(formula: Formula) -> Set[Formula]:
        if isinstance(formula, Or):
            return collect_disjuncts(formula.left) | collect_disjuncts(formula.right)
        else:
            return { formula }

    # Only one supporting step should be cited
    if len(supports) != 1:
        return False
    support = supports[0]

    # Supporting step should be a statement
    if not isinstance(support, Statement):
        return False

    # Collect disjuncts from statement
    disjuncts = collect_disjuncts(statement.formula)

    # Support should show up somewhere in the statement
    return support.formula in disjuncts

def not_introduction_rule(supports: List[Step], statement: Statement) -> bool:
    # Only one supporting step should be cited
    if len(supports) != 1:
        return False
    support = supports[0]

    # Supporting step should be a subproof
    if not isinstance(support, Subproof):
        return False
    
    # Statement should be a not
    if not isinstance(statement.formula, Not):
        return False
    
    # Supporting assumption should be the inverted statement
    inv_statement_formula = statement.formula.value
    if support.assumption.formula != inv_statement_formula:
        return False
    
    # There should be a bottom in the proof somewhere
    for step in support.steps:
        if not isinstance(step, Statement):
            continue
        if isinstance(step.formula, Bottom):
            return True
    return False

def bottom_introduction_rule(supports: List[Step], statement: Statement) -> bool:
    # Two support steps should be cited
    if len(supports) != 2:
        return False
    support1, support2 = supports

    # Each step should be a statement
    if not isinstance(support1, Statement) or not isinstance(support2, Statement):
        return False
    
    # One of them should be the negation of the other
    if not (Not(support1.formula) == support2.formula or support1.formula == Not(support2.formula)):
        return False
    
    # The statement should just be the bottom
    return statement.formula == Bottom()

def conditional_introduction_rule(supports: List[Step], statement: Statement) -> bool:
    # Must have exactly one support
    if len(supports) != 1:
        return False
    support = supports[0]

    # Must be a subproof
    if not isinstance(support, Subproof):
        return False

    # Subproof must have at least one step
    if not support.steps:
        return False

    # Get antecedent and consequent
    antecedent = support.assumption.formula
    last_step = support.steps[-1]
    if not isinstance(last_step, Statement):
        return False
    consequent = last_step.formula

    # Conclusion must be antecedent → consequent
    return statement.formula == Implies(antecedent, consequent)


def biconditional_introduction_rule(supports: List[Step], statement: Statement) -> bool:
    # Two supporting steps
    if len(supports) != 2:
        return False

    # Both must be subproofs
    a, b = supports
    if not isinstance(a, Subproof) or not isinstance(b, Subproof):
        return False

    # Both must have steps
    if not a.steps or not b.steps:
        return False

    # Both should end with a statement
    if not isinstance(a.steps[-1], Statement) or not isinstance(b.steps[-1], Statement):
        return False

    # Get bidirectional assumptions and conclusions
    a_assume, a_conclude = a.assumption.formula, a.steps[-1].formula
    b_assume, b_conclude = b.assumption.formula, b.steps[-1].formula

    # Valid if: a = P ⇒ Q and b = Q ⇒ P (or reversed)
    expected1 = Iff(a_assume, a_conclude)
    expected2 = Iff(b_conclude, b_assume)

    return statement.formula == expected1 or statement.formula == expected2
