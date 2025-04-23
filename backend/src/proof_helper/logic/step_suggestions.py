from typing import List, Tuple
from itertools import combinations
from proof_helper.core.proof import Step, Statement, Subproof, Proof
from proof_helper.core.formula import Formula
from proof_helper.logic.rule_registry import RuleRegistry
from proof_helper.logic.rules_base import Rule
from proof_helper.logic.formula_similarity import score_similarity

def generate_next_steps(proof: Proof, registry: RuleRegistry) -> List[Tuple[Statement, float]]:
    suggestions: List[Tuple[Statement, float]] = []
    all_steps = proof.premises + proof.steps

    for rule in registry.get_all_rules():
        
        expected = rule.num_supports()

        # Skip if not enough statements to satisfy fixed-arity rules
        if expected is not None and len(all_steps) < expected:
            continue

        from itertools import combinations
        support_sets = (
            combinations(all_steps, expected)
            if expected is not None
            else [all_steps]
        )

        for support_set in support_sets:
            if not rule.is_applicable(list(support_set)):
                continue

            # Use conclude() to generate possible resulting formulas
            if rule.name() in { "Or Introduction" }:
                new_formulas = rule.conclude(list(support_set), [c.formula for c in proof.conclusions] or None)
            else:
                new_formulas = rule.conclude(list(support_set))

            for f in new_formulas:
                stmt = Statement(
                    id=None,
                    formula=f,
                    rule=rule.name(),
                    premises=[s.id for s in support_set],
                )
                score = (
                    max(score_similarity(f, c.formula) for c in proof.conclusions)
                    if proof.conclusions
                    else 0
                )
                suggestions.append((stmt, score))

    suggestions.sort(key=lambda pair: -pair[1])
    return suggestions
