import pytest
from proof_helper.formula import Variable, And, Or, Bottom, Not
from proof_helper.proof import Proof, StepID, Statement, Subproof, Step
from proof_helper.rules import RuleChecker
from proof_helper.verify import verify_statement, verify_subproof, verify_step, verify_proof

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
    checker = RuleChecker()
    assert verify_statement(s, proof, checker)

def test_invalid_rule_returns_false():
    P = Variable("P")
    s = stmt("1", P, rule="Gibberish")
    proof = fake_proof(steps=[s])
    checker = RuleChecker()
    assert not verify_statement(s, proof, checker)

def test_none_rule_returns_false():
    P = Variable("P")
    s = stmt("1", P, rule=None)
    proof = fake_proof(steps=[s])
    checker = RuleChecker()
    assert not verify_statement(s, proof, checker)

def test_valid_and_intro():
    P = Variable("P")
    Q = Variable("Q")
    a = stmt("1", P, rule="Assumption")
    b = stmt("2", Q, rule="Assumption")
    ab = stmt("3", And(P, Q), rule="∧ Introduction", premises=[sid("1"), sid("2")])
    proof = fake_proof(premises=[a, b], steps=[ab])
    checker = RuleChecker()
    assert verify_statement(ab, proof, checker)

def test_invalid_and_intro_wrong_formula():
    P = Variable("P")
    Q = Variable("Q")
    a = stmt("1", P, rule="Assumption")
    b = stmt("2", Q, rule="Assumption")
    wrong = stmt("3", Variable("X"), rule="∧ Introduction", premises=[sid("1"), sid("2")])
    proof = fake_proof(premises=[a, b], steps=[wrong])
    checker = RuleChecker()
    assert not verify_statement(wrong, proof, checker)

def test_invalid_missing_premise():
    P = Variable("P")
    a = stmt("1", P, rule="Assumption")
    b = stmt("2", P, rule="∨ Introduction", premises=[sid("1"), sid("999")])  # 999 doesn't exist
    proof = fake_proof(premises=[a], steps=[b])
    checker = RuleChecker()
    assert not verify_statement(b, proof, checker)

def test_valid_bottom_elimination():
    bottom = stmt("1", Bottom(), rule="Assumption")
    result = stmt("2", Variable("X"), rule="⊥ Elimination", premises=[sid("1")])
    proof = fake_proof(premises=[bottom], steps=[result])
    checker = RuleChecker()
    assert verify_statement(result, proof, checker)

# === VERIFY SUBPROOF ===

def test_invalid_subproof_with_invalid_assumption():
    X = Variable("X")

    assume = stmt("1.1", X, rule="???")  # invalid rule
    step = stmt("1.2", X, rule="Assumption")
    sp = subproof("1", assume, [step])
    proof = fake_proof()
    checker = RuleChecker()
    assert not verify_subproof(sp, proof, checker)

def test_invalid_subproof_with_invalid_inner_step():
    P = Variable("P")
    assume = stmt("1.1", P, rule="Assumption")
    step = stmt("1.2", P, rule="???", premises=[sid("1.1")])  # invalid rule

    sp = subproof("1", assume, [step])
    proof = fake_proof()
    checker = RuleChecker()
    assert not verify_subproof(sp, proof, checker)

def test_empty_subproof_is_valid_if_assumption_is_valid():
    A = Variable("A")
    assume = stmt("1.1", A, rule="Assumption")
    sp = subproof("1", assume, steps=[])
    proof = fake_proof()
    checker = RuleChecker()
    assert verify_subproof(sp, proof, checker)

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

    checker = RuleChecker()
    assert verify_proof(proof, checker)

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

    checker = RuleChecker()

    assert not verify_proof(proof, checker)

def test_invalid_proof_with_wrong_conclusion():
    P = Variable("P")

    s = stmt("1", P, rule="Assumption")
    bad = stmt("2", Not(P), rule="¬ Introduction", premises=[sid("1")])

    proof = Proof(
        premises=[s],
        steps=[bad],
        conclusions=[bad]
    )

    checker = RuleChecker()

    assert not verify_proof(proof, checker)

def test_invalid_premise_rule():
    P = Variable("P")
    bad_premise = stmt("1", P, rule="∨ Introduction")  # not Assumption
    proof = Proof(premises=[bad_premise], steps=[], conclusions=[])
    checker = RuleChecker()
    assert not verify_proof(proof, checker)

def test_invalid_conclusion_rule():
    P = Variable("P")
    good = stmt("1", P, rule="Assumption")
    derived = stmt("2", P, rule="Reiteration", premises=[sid("1")])
    bad_conclusion = stmt("3", P, rule="∧ Introduction", premises=[sid("1"), sid("1")])
    proof = Proof(premises=[good], steps=[derived], conclusions=[bad_conclusion])
    checker = RuleChecker()
    assert not verify_proof(proof, checker)

def test_invalid_subproof_assumption_rule():
    P = Variable("P")
    assume = stmt("1.1", P, rule="¬ Introduction")  # not Assumption
    step = stmt("1.2", Bottom(), rule="⊥ Introduction", premises=[sid("1.1"), sid("1.1")])
    sp = subproof("1", assume, [step])
    reiterate = stmt("2", Bottom(), rule="Reiteration", premises=[sid("1.2")])
    proof = Proof(premises=[], steps=[assume, step, sp, reiterate], conclusions=[reiterate])
    checker = RuleChecker()
    assert not verify_proof(proof, checker)

def test_valid_conjunction_with_reiteration():
    P = Variable("P")
    Q = Variable("Q")

    a = stmt("1", P, rule="Assumption")
    b = stmt("2", Q, rule="Assumption")
    conj = stmt("3", And(P, Q), rule="∧ Introduction", premises=[sid("1"), sid("2")])
    reiterate = stmt("4", And(P, Q), rule="Reiteration", premises=[sid("3")])
    proof = Proof(premises=[a, b], steps=[conj], conclusions=[reiterate])
    checker = RuleChecker()
    assert verify_proof(proof, checker)
