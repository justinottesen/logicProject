from typing import List
from proof_helper.proof import Proof, StepID
from proof_helper.proof import Statement, Subproof, Step
from proof_helper.rules import RuleChecker

def verify_statement(statement: Statement, proof: Proof, checker: RuleChecker) -> bool:
    if statement.rule is None or not checker.has(statement.rule):
        return False

    supports: List[Step] = []
    for pid in statement.premises:
        step = proof.get_step(pid)
        if step is None:
            return False
        supports.append(step)

    rule_fn = checker.get(statement.rule)
    return rule_fn(supports, statement)

def verify_subproof(subproof: Subproof, proof: Proof, checker: RuleChecker) -> bool:
    if not verify_statement(subproof.assumption, proof, checker):
        return False
    for step in subproof.steps:
        if not verify_step(step, proof, checker):
            return False
    return True

def verify_step(step: Step, proof: Proof, checker: RuleChecker) -> bool:
    if isinstance(step, Statement):
        return verify_statement(step, proof, checker)
    elif isinstance(step, Subproof):
        return verify_subproof(step, proof, checker)
    return False

def verify_proof(proof: Proof, checker: RuleChecker) -> bool:
    for premise in proof.premises:
        if not verify_statement(premise, proof, checker):
            return False
    for step in proof.steps:
        if not verify_step(step, proof, checker):
            return False
    for conclusion in proof.conclusions:
        if not verify_statement(conclusion, proof, checker):
            return False

    return True
