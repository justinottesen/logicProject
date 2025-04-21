import pytest
from proof_helper.core.formula import Variable, And, Or, Bottom, Not
from proof_helper.core.proof import Proof, StepID, Statement, Subproof, Step
from proof_helper.logic.rule_registry import RuleRegistry
from proof_helper.logic.verify import VerificationError, verify_statement, verify_subproof, verify_step, verify_proof

# === Helpers ===

def sid(s: str) -> StepID:
    return StepID.from_string(s)

def stmt(id: str, formula, rule=None, premises=None):
    return Statement(id=sid(id), formula=formula, rule=rule, premises=premises or [])

def subproof(id: str, assumption: Statement, steps):
    return Subproof(id=sid(id), assumption=assumption, steps=steps)

def fake_proof(premises=None, steps=None, conclusions=None) -> Proof:
    return Proof(
        premises=premises or [],
        steps=steps or [],
        conclusions=conclusions or []
    )

# === VERIFY STATEMENT ===

def test_assumption_is_always_valid():
    P = Variable("P")
    s = stmt("1", P, rule="Assumption")
    proof = fake_proof(premises=[s])
    rule_checker = RuleRegistry()
    assert verify_statement(s, proof, rule_checker)

def test_invalid_rule_returns_false():
    P = Variable("P")
    s = stmt("1", P, rule="Gibberish")
    proof = fake_proof(steps=[s])
    rule_checker = RuleRegistry()
    result = verify_statement(s, proof, rule_checker)
    assert isinstance(result, VerificationError)

def test_none_rule_returns_false():
    P = Variable("P")
    s = stmt("1", P, rule=None)
    proof = fake_proof(steps=[s])
    rule_checker = RuleRegistry()
    result = verify_statement(s, proof, rule_checker)
    assert isinstance(result, VerificationError)

def test_valid_and_intro():
    P = Variable("P")
    Q = Variable("Q")
    a = stmt("1", P, rule="Assumption")
    b = stmt("2", Q, rule="Assumption")
    ab = stmt("3", And(P, Q), rule="∧ Introduction", premises=[sid("1"), sid("2")])
    proof = fake_proof(premises=[a, b], steps=[ab])
    rule_checker = RuleRegistry()
    assert verify_statement(ab, proof, rule_checker)

def test_invalid_and_intro_wrong_formula():
    P = Variable("P")
    Q = Variable("Q")
    a = stmt("1", P, rule="Assumption")
    b = stmt("2", Q, rule="Assumption")
    wrong = stmt("3", Variable("X"), rule="∧ Introduction", premises=[sid("1"), sid("2")])
    proof = fake_proof(premises=[a, b], steps=[wrong])
    rule_checker = RuleRegistry()
    result = verify_statement(wrong, proof, rule_checker)
    assert isinstance(result, VerificationError)

def test_invalid_missing_premise():
    P = Variable("P")
    a = stmt("1", P, rule="Assumption")
    b = stmt("2", P, rule="∨ Introduction", premises=[sid("1"), sid("999")])  # 999 doesn't exist
    proof = fake_proof(premises=[a], steps=[b])
    rule_checker = RuleRegistry()
    result = verify_statement(b, proof, rule_checker)
    assert isinstance(result, VerificationError)

def test_valid_bottom_elimination():
    bottom = stmt("1", Bottom(), rule="Assumption")
    result = stmt("2", Variable("X"), rule="⊥ Elimination", premises=[sid("1")])
    proof = fake_proof(premises=[bottom], steps=[result])
    rule_checker = RuleRegistry()
    assert verify_statement(result, proof, rule_checker)

# === VERIFY SUBPROOF ===

def test_invalid_subproof_with_invalid_assumption():
    X = Variable("X")

    assume = stmt("1.1", X, rule="???")  # invalid rule
    step = stmt("1.2", X, rule="Assumption")
    sp = subproof("1", assume, [step])
    proof = fake_proof()
    rule_checker = RuleRegistry()
    result = verify_subproof(sp, proof, rule_checker)
    assert isinstance(result, VerificationError)

def test_invalid_subproof_with_invalid_inner_step():
    P = Variable("P")
    assume = stmt("1.1", P, rule="Assumption")
    step = stmt("1.2", P, rule="???", premises=[sid("1.1")])  # invalid rule

    sp = subproof("1", assume, [step])
    proof = fake_proof()
    rule_checker = RuleRegistry()
    result = verify_subproof(sp, proof, rule_checker)
    assert isinstance(result, VerificationError)

def test_empty_subproof_is_valid_if_assumption_is_valid():
    A = Variable("A")
    assume = stmt("1.1", A, rule="Assumption")
    sp = subproof("1", assume, steps=[])
    proof = fake_proof()
    rule_checker = RuleRegistry()
    assert verify_subproof(sp, proof, rule_checker)

# === VERIFY PROOF ===

def test_valid_full_proof_with_not_intro():
    P = Variable("P")

    # Step 1: ¬P (Premise)
    not_P = stmt("1", Not(P), rule="Assumption")

    # Subproof: Assume P
    assume_P = stmt("2.1", P, rule="Assumption")

    # Derive ⊥ from P and ¬P
    contradiction = stmt("2.2", Bottom(), rule="⊥ Introduction", premises=[sid("1"), sid("2.1")])
    sp = subproof("2", assume_P, [contradiction])

    proof = Proof(
        premises=[not_P],
        steps=[assume_P, contradiction, sp],
        conclusions=[]
    )

    rule_checker = RuleRegistry()
    assert verify_proof(proof, rule_checker)

def test_invalid_proof_with_missing_premise():
    P = Variable("P")
    Q = Variable("Q")

    # Step 1 is missing
    and_intro = stmt("2", Variable("R"), rule="∧ Introduction", premises=[sid("1"), sid("99")])

    proof = Proof(
        premises=[],
        steps=[and_intro],
        conclusions=[]
    )

    rule_checker = RuleRegistry()

    result = verify_proof(proof, rule_checker)
    assert isinstance(result, VerificationError)

def test_invalid_proof_with_wrong_conclusion():
    P = Variable("P")

    s = stmt("1", P, rule="Assumption")
    bad = stmt("2", Not(P), rule="¬ Introduction", premises=[sid("1")])

    proof = Proof(
        premises=[s],
        steps=[bad],
        conclusions=[bad]
    )

    rule_checker = RuleRegistry()

    result = verify_proof(proof, rule_checker)
    assert isinstance(result, VerificationError)

def test_invalid_premise_rule():
    P = Variable("P")
    bad_premise = stmt("1", P, rule="∨ Introduction")  # not Assumption
    proof = Proof(premises=[bad_premise], steps=[], conclusions=[])
    rule_checker = RuleRegistry()
    result = verify_proof(proof, rule_checker)
    assert isinstance(result, VerificationError)

def test_invalid_conclusion_rule():
    P = Variable("P")
    good = stmt("1", P, rule="Assumption")
    derived = stmt("2", P, rule="Reiteration", premises=[sid("1")])
    bad_conclusion = stmt("3", P, rule="∧ Introduction", premises=[sid("1"), sid("1")])
    proof = Proof(premises=[good], steps=[derived], conclusions=[bad_conclusion])
    rule_checker = RuleRegistry()
    result = verify_proof(proof, rule_checker)
    assert isinstance(result, VerificationError)

def test_invalid_subproof_assumption_rule():
    P = Variable("P")
    assume = stmt("1.1", P, rule="¬ Introduction")  # not Assumption
    step = stmt("1.2", Bottom(), rule="⊥ Introduction", premises=[sid("1.1"), sid("1.1")])
    sp = subproof("1", assume, [step])
    reiterate = stmt("2", Bottom(), rule="Reiteration", premises=[sid("1.2")])
    proof = Proof(premises=[], steps=[assume, step, sp, reiterate], conclusions=[reiterate])
    rule_checker = RuleRegistry()
    result = verify_proof(proof, rule_checker)
    assert isinstance(result, VerificationError)

def test_valid_conjunction_with_reiteration():
    P = Variable("P")
    Q = Variable("Q")

    a = stmt("1", P, rule="Assumption")
    b = stmt("2", Q, rule="Assumption")
    conj = stmt("3", And(P, Q), rule="∧ Introduction", premises=[sid("1"), sid("2")])
    reiterate = stmt("4", And(P, Q), rule="Reiteration", premises=[sid("3")])
    proof = Proof(premises=[a, b], steps=[conj], conclusions=[reiterate])
    rule_checker = RuleRegistry()
    assert verify_proof(proof, rule_checker)

# === VERIFY WITH CUSTOM RULES ===

def test_verify_proof_with_custom_rule_success():
    P = Variable("P")
    Q = Variable("Q")
    A = stmt("1", P, rule="Assumption")
    B = stmt("2", Q, rule="Assumption")
    AB = stmt("3", And(P, Q), rule="∧ Introduction", premises=[sid("1"), sid("2")])

    # Define the custom rule proof
    custom_proof = Proof(premises=[A, B], steps=[AB], conclusions=[AB])
    registry = RuleRegistry()
    registry.add_custom_rule("MyConjunction", custom_proof)

    # Use the custom rule
    a2 = stmt("1", P, rule="Assumption")
    b2 = stmt("2", Q, rule="Assumption")
    conj2 = stmt("3", And(P, Q), rule="MyConjunction", premises=[sid("1"), sid("2")])
    reiterate = stmt("4", And(P, Q), rule="Reiteration", premises=[sid("3")])

    proof = Proof(premises=[a2, b2], steps=[conj2], conclusions=[reiterate])
    result = verify_proof(proof, registry)
    assert result is True

def test_verify_custom_rule_wrong_premises():
    P = Variable("P")
    Q = Variable("Q")
    R = Variable("R")

    A = stmt("1", P, rule="Assumption")
    B = stmt("2", Q, rule="Assumption")
    AB = stmt("3", And(P, Q), rule="∧ Introduction", premises=[sid("1"), sid("2")])
    custom_proof = Proof(premises=[A, B], steps=[AB], conclusions=[AB])

    registry = RuleRegistry()
    registry.add_custom_rule("MyConjunction", custom_proof)

    # One wrong premise
    p = stmt("1", P, rule="Assumption")
    r = stmt("2", R, rule="Assumption")
    wrong_conj = stmt("3", And(P, Q), rule="MyConjunction", premises=[sid("1"), sid("2")])
    reiterate = stmt("4", And(P, Q), rule="Reiteration", premises=[sid("3")])

    proof = Proof(premises=[p, r], steps=[wrong_conj], conclusions=[reiterate])
    result = verify_proof(proof, registry)
    assert isinstance(result, VerificationError)
    assert result.step_id == "3"

def test_verify_custom_rule_unknown_name():
    P = Variable("P")
    Q = Variable("Q")

    p = stmt("1", P, rule="Assumption")
    q = stmt("2", Q, rule="Assumption")
    bad = stmt("3", And(P, Q), rule="UnknownRule", premises=[sid("1"), sid("2")])
    reiterate = stmt("4", And(P, Q), rule="Reiteration", premises=[sid("3")])

    proof = Proof(premises=[p, q], steps=[bad], conclusions=[reiterate])
    registry = RuleRegistry()
    result = verify_proof(proof, registry)
    assert isinstance(result, VerificationError)
    assert result.step_id == "3"
