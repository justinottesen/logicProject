import pytest
from proof_helper.core.formula import Variable, And, Or, Bottom, Not, Implies
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
    assert verify_statement(s, proof, rule_checker) is True

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
    ab = stmt("3", And(P, Q), rule="And Introduction", premises=[sid("1"), sid("2")])
    proof = fake_proof(premises=[a, b], steps=[ab])
    rule_checker = RuleRegistry()
    assert verify_statement(ab, proof, rule_checker) is True

def test_invalid_and_intro_wrong_formula():
    P = Variable("P")
    Q = Variable("Q")
    a = stmt("1", P, rule="Assumption")
    b = stmt("2", Q, rule="Assumption")
    wrong = stmt("3", Variable("X"), rule="And Introduction", premises=[sid("1"), sid("2")])
    proof = fake_proof(premises=[a, b], steps=[wrong])
    rule_checker = RuleRegistry()
    result = verify_statement(wrong, proof, rule_checker)
    assert isinstance(result, VerificationError)

def test_invalid_missing_premise():
    P = Variable("P")
    a = stmt("1", P, rule="Assumption")
    b = stmt("2", P, rule="Or Introduction", premises=[sid("1"), sid("999")])  # 999 doesn't exist
    proof = fake_proof(premises=[a], steps=[b])
    rule_checker = RuleRegistry()
    result = verify_statement(b, proof, rule_checker)
    assert isinstance(result, VerificationError)

def test_valid_bottom_elimination():
    bottom = stmt("1", Bottom(), rule="Assumption")
    result = stmt("2", Variable("X"), rule="Bottom Elimination", premises=[sid("1")])
    proof = fake_proof(premises=[bottom], steps=[result])
    rule_checker = RuleRegistry()
    assert verify_statement(result, proof, rule_checker) is True

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
    assert verify_subproof(sp, proof, rule_checker) is True

# === VERIFY PROOF ===

def test_valid_full_proof_with_not_intro():
    P = Variable("P")

    # Step 1: ¬P (Premise)
    not_P = stmt("1", Not(P), rule="Assumption")

    # Subproof: Assume P
    assume_P = stmt("2.1", P, rule="Assumption")

    # Derive ⊥ from P and ¬P
    contradiction = stmt("2.2", Bottom(), rule="Bottom Introduction", premises=[sid("1"), sid("2.1")])
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
    and_intro = stmt("2", Variable("R"), rule="And Introduction", premises=[sid("1"), sid("99")])

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
    bad = stmt("2", Not(P), rule="Not Introduction", premises=[sid("1")])

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
    bad_premise = stmt("1", P, rule="Or Introduction")  # not Assumption
    proof = Proof(premises=[bad_premise], steps=[], conclusions=[])
    rule_checker = RuleRegistry()
    result = verify_proof(proof, rule_checker)
    assert isinstance(result, VerificationError)

def test_invalid_conclusion_rule():
    P = Variable("P")
    good = stmt("1", P, rule="Assumption")
    derived = stmt("2", P, rule="Reiteration", premises=[sid("1")])
    bad_conclusion = stmt("3", P, rule="And Introduction", premises=[sid("1"), sid("1")])
    proof = Proof(premises=[good], steps=[derived], conclusions=[bad_conclusion])
    rule_checker = RuleRegistry()
    result = verify_proof(proof, rule_checker)
    assert isinstance(result, VerificationError)

def test_invalid_subproof_assumption_rule():
    P = Variable("P")
    assume = stmt("1.1", P, rule="Not Introduction")  # not Assumption
    step = stmt("1.2", Bottom(), rule="Bottom Introduction", premises=[sid("1.1"), sid("1.1")])
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
    conj = stmt("3", And(P, Q), rule="And Introduction", premises=[sid("1"), sid("2")])
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
    AB = stmt("3", And(P, Q), rule="And Introduction", premises=[sid("1"), sid("2")])

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
    AB = stmt("3", And(P, Q), rule="And Introduction", premises=[sid("1"), sid("2")])
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

def test_verify_proof_with_excluded_middle_custom_rule():
    P = Variable("P")
    Q = Variable("Q")

    disj = Or(P, Not(P))

    # Step 1.1: ¬(P ∨ ¬P)
    not_disj = Statement(sid("1.1"), Not(disj), "Assumption")

    # Subproof 1.2: assume P
    assume_p = Statement(sid("1.2.1"), P, "Assumption")
    or_intro_1 = Statement(sid("1.2.2"), disj, "Or Introduction", [sid("1.2.1")])
    bottom_1 = Statement(sid("1.2.3"), Bottom(), "Bottom Introduction", [sid("1.1"), sid("1.2.2")])
    subproof_1_2 = Subproof(sid("1.2"), assume_p, [or_intro_1, bottom_1])

    # Step 1.3: ¬P by Not Introduction from subproof 1.2
    not_p = Statement(sid("1.3"), Not(P), "Not Introduction", [sid("1.2")])

    # Step 1.4: P ∨ ¬P by Or Introduction on ¬P
    or_intro_2 = Statement(sid("1.4"), disj, "Or Introduction", [sid("1.3")])

    # Step 1.5: ⊥ from 1.1 and 1.4
    bottom_2 = Statement(sid("1.5"), Bottom(), "Bottom Introduction", [sid("1.1"), sid("1.4")])

    # Subproof 1
    subproof_1 = Subproof(sid("1"), not_disj, [subproof_1_2, not_p, or_intro_2, bottom_2])

    # Step 2: ¬¬(P ∨ ¬P) by Not Introduction from 1
    not_not_disj = Statement(sid("2"), Not(Not(disj)), "Not Introduction", [sid("1")])

    # Step 3: P ∨ ¬P by Not Elimination on 2
    conclusion_step = Statement(sid("3"), disj, "Not Elimination", [sid("2")])

    # Step 4: reiterate 3
    reiteration = Statement(sid("4"), disj, "Reiteration", [sid("3")])

    excluded_middle = Proof(
        premises=[],
        steps=[subproof_1, not_not_disj, conclusion_step],
        conclusions=[reiteration]
    )
    registry = RuleRegistry()
    assert verify_proof(excluded_middle, registry) is True
    registry.add_custom_rule("ExcludedMiddle", excluded_middle)

    # Construct a user proof using this custom rule
    implication = stmt("1", Implies(Or(P, Not(P)), Q), rule="Assumption")
    use_em = stmt("2", Or(P, Not(P)), rule="ExcludedMiddle", premises=[])
    apply_impl = stmt("3", Q, rule="Implication Elimination", premises=[sid("1"), sid("2")])
    final = stmt("4", Q, rule="Reiteration", premises=[sid("3")])

    user_proof = Proof(
        premises=[implication],
        steps=[use_em, apply_impl],
        conclusions=[final]
    )

    assert verify_proof(user_proof, registry) is True
