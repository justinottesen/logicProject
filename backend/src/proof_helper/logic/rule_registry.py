from typing import Dict, Optional
from proof_helper.logic.rules_builtin import (
    RuleFn, rule_wrapper,
    assumption_rule, reiteration_rule,
    and_introduction_rule, and_elimination_rule,
    or_introduction_rule, or_elimination_rule,
    not_introduction_rule, not_elimination_rule,
    bottom_introduction_rule, bottom_elimination_rule,
    conditional_introduction_rule, conditional_elimination_rule,
    biconditional_introduction_rule, biconditional_elimination_rule,
)
from proof_helper.logic.rules_custom import CustomRule
from proof_helper.core.proof import Proof
from proof_helper.io.rule_storage import CustomRuleStore

class RuleRegistry:
    def __init__(self, custom_rule_store: Optional[CustomRuleStore] = None):
        self.rules: Dict[str, RuleFn] = {
            # Assumption - For premises & subproof assumptions
            "Assumption": rule_wrapper(assumption_rule),
            # Reiteration
            "Reiteration": rule_wrapper(reiteration_rule),
            # Introduction Rules
            "∧ Introduction": rule_wrapper(and_introduction_rule),
            "∨ Introduction": rule_wrapper(or_introduction_rule),
            "¬ Introduction": rule_wrapper(not_introduction_rule),
            "⊥ Introduction": rule_wrapper(bottom_introduction_rule),
            "→ Introduction": rule_wrapper(conditional_introduction_rule),
            "↔ Introduction": rule_wrapper(biconditional_introduction_rule),
            # Elimination Rules
            "∧ Elimination": rule_wrapper(and_elimination_rule),
            "∨ Elimination": rule_wrapper(or_elimination_rule),
            "¬ Elimination": rule_wrapper(not_elimination_rule),
            "⊥ Elimination": rule_wrapper(bottom_elimination_rule),
            "→ Elimination": rule_wrapper(conditional_elimination_rule),
            "↔ Elimination": rule_wrapper(biconditional_elimination_rule),
        }

        self.custom_rules: Dict[str, CustomRule] = {}
        if custom_rule_store:
            for name, proof in custom_rule_store.list_rules().items():
                self.custom_rules[name] = CustomRule(name, proof)

    def add_custom_rule(self, name: str, proof: Proof):
        if name in self.rules or name in self.custom_rules:
            raise ValueError(f"Rule '{name}' already exists")

        rule = CustomRule(name, proof)
        self.custom_rules[name] = rule

    def get(self, name: str) -> RuleFn:
        if name in self.rules:
            return self.rules[name]
        if name in self.custom_rules:
            return self.custom_rules[name]
        raise KeyError(f"Rule '{name}' not found")

    def has(self, name: str) -> bool:
        return name in self.rules or name in self.custom_rules