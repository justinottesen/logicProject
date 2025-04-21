from functools import wraps
from typing import Callable, Dict, List, Set
from proof_helper.proof import Step, Statement
from proof_helper.formula import Formula, Variable, And, Or

# Each rule takes premises + subproofs and returns a derived formula
RuleFn = Callable[[List[Step], Statement], bool]

class RuleChecker:
    def __init__(self):
        self.rules: Dict[str, RuleFn] = {
            "Assumption": rule_wrapper(assumption_rule),
            "∧ Introduction": rule_wrapper(and_introduction_rule),
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
            print("A")
            return False
        # Sanity check of type
        if not isinstance(statement, Statement):
            print("B")
            return False
        # Supporting steps must be before the statement
        for support in supports:
            if not support.id.is_before(statement.id):
                print("C")
                return False
        # Supporting steps must match statement premises
        if set(map(lambda x: x.id, supports)) != set(statement.premises):
            for x in map(lambda x: x.id, supports):
                print(x)
            print()
            for x in statement.premises:
                print(x)
            print("D")
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