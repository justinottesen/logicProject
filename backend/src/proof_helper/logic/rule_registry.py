from typing import Dict, Optional
from proof_helper.core.proof import Step, Statement, Proof
from proof_helper.logic.rules_base import Rule
from proof_helper.logic.rules_builtin import BUILTIN_RULES
from proof_helper.logic.rules_custom import CustomRule
from proof_helper.io.rule_storage import CustomRuleStore


class RuleRegistry:
    def __init__(self, custom_rule_store: Optional[CustomRuleStore] = None):
        self.rules: Dict[str, Rule] = {
            rule.name(): rule for rule in BUILTIN_RULES
        }

        self.custom_rules: Dict[str, CustomRule] = {}
        if custom_rule_store:
            for name, proof in custom_rule_store.list_rules().items():
                self.custom_rules[name] = CustomRule(name, proof)

    def add_custom_rule(self, name: str, proof: Proof):
        if name in self.rules or name in self.custom_rules:
            raise ValueError(f"Rule '{name}' already exists")
        self.custom_rules[name] = CustomRule(name, proof)

    def get(self, name: str) -> Rule:
        if name in self.rules:
            return self.rules[name]
        if name in self.custom_rules:
            return self.custom_rules[name]
        raise KeyError(f"Rule '{name}' not found")

    def has(self, name: str) -> bool:
        return name in self.rules or name in self.custom_rules