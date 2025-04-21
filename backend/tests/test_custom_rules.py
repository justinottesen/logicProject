import pytest
from proof_helper.logic.rules_custom import CustomRule
from proof_helper.core.proof import Proof, StepID, Statement
from proof_helper.core.formula import Variable, And

def sid(s: str) -> StepID:
    return StepID.from_string(s)

def stmt(id: str, formula, rule=None, premises=None):
    return Statement(id=sid(id), formula=formula, rule=rule, premises=premises or [])

def test_custom_rule_and_intro_success():
    P = Variable("P")
    Q = Variable("Q")
    A = stmt("1", P, rule="Assumption")
    B = stmt("2", Q, rule="Assumption")
    AB = stmt("3", And(P, Q), rule="∧ Introduction", premises=[sid("1"), sid("2")])

    proof = Proof(premises=[A, B], steps=[AB], conclusions=[AB])
    rule = CustomRule("Test ∧ Intro", proof)

    result = rule([A, B], AB)
    assert result is True

def test_custom_rule_wrong_premise_formula():
    P = Variable("P")
    Q = Variable("Q")
    R = Variable("R")
    A = stmt("1", P, rule="Assumption")
    B = stmt("2", Q, rule="Assumption")
    AB = stmt("3", And(P, Q), rule="∧ Introduction", premises=[sid("1"), sid("2")])

    proof = Proof(premises=[A, B], steps=[AB], conclusions=[AB])
    rule = CustomRule("Test ∧ Intro", proof)

    bad = stmt("0", R, rule="Assumption")
    result = rule([A, bad], AB)
    assert result is False

def test_custom_rule_wrong_conclusion_formula():
    P = Variable("P")
    Q = Variable("Q")
    A = stmt("1", P, rule="Assumption")
    B = stmt("2", Q, rule="Assumption")
    AB = stmt("3", And(P, Q), rule="∧ Introduction", premises=[sid("1"), sid("2")])
    Wrong = stmt("4", P, rule="Reiteration", premises=[sid("1")])

    proof = Proof(premises=[A, B], steps=[AB], conclusions=[AB])
    rule = CustomRule("Test ∧ Intro", proof)

    result = rule([A, B], Wrong)
    assert result is False

