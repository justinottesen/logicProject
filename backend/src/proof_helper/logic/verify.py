from typing import List, Union, NamedTuple
from proof_helper.core.proof import Proof, StepID
from proof_helper.core.proof import Statement, Subproof, Step
from proof_helper.logic.rules_builtin import RuleRegistry

class VerificationError(NamedTuple):
    step_id: str
    message: str

VerificationResult = Union[bool, VerificationError]

def verify_statement(statement: Statement, proof: Proof, rule_checker: RuleRegistry) -> VerificationResult:
    if statement.rule is None:
        return VerificationError(str(statement.id), "Missing rule on statement")

    if not rule_checker.has(statement.rule):
        return VerificationError(str(statement.id), f"Unknown rule: {statement.rule}")

    supports: List[Step] = []
    for pid in statement.premises:
        step = proof.get_step(pid)
        if step is None:
            return VerificationError(str(statement.id), f"Referenced step {pid} not found")
        supports.append(step)

    rule_fn = rule_checker.get(statement.rule)
    if not rule_fn(supports, statement):
        return VerificationError(str(statement.id), f"Rule {statement.rule} failed to apply")

    return True

def verify_subproof(subproof: Subproof, proof: Proof, rule_checker: RuleRegistry) -> VerificationResult:
    if not isinstance(subproof.assumption, Statement):
        return VerificationError(str(subproof.id), "Subproof assumption must be a Statement")

    if subproof.assumption.rule != "Assumption":
        return VerificationError(str(subproof.assumption.id), "Subproof assumption must use rule 'Assumption'")

    result = verify_statement(subproof.assumption, proof, rule_checker)
    if result is not True:
        return result

    for step in subproof.steps:
        result = verify_step(step, proof, rule_checker)
        if result is not True:
            return result

    return True

def verify_step(step: Step, proof: Proof, rule_checker: RuleRegistry) -> VerificationResult:
    if isinstance(step, Statement):
        return verify_statement(step, proof, rule_checker)
    elif isinstance(step, Subproof):
        return verify_subproof(step, proof, rule_checker)
    return VerificationError("?", "Step is neither Statement nor Subproof")

def verify_proof(proof: Proof, rule_checker: RuleRegistry) -> VerificationResult:
    for premise in proof.premises:
        if not isinstance(premise, Statement):
            return VerificationError(str(premise.id), "Premise must be a Statement")

        if premise.rule != "Assumption":
            return VerificationError(str(premise.id), "Premise must use rule 'Assumption'")

        result = verify_statement(premise, proof, rule_checker)
        if result is not True:
            return result

    for step in proof.steps:
        result = verify_step(step, proof, rule_checker)
        if result is not True:
            return result

    for conclusion in proof.conclusions:
        if not isinstance(conclusion, Statement):
            return VerificationError(str(conclusion.id), "Conclusion must be a Statement")

        if conclusion.rule != "Reiteration":
            return VerificationError(str(conclusion.id), "Conclusion must use rule 'Reiteration'")

        result = verify_statement(conclusion, proof, rule_checker)
        if result is not True:
            return result

    return True