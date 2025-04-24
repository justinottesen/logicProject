import pytest
from proof_helper.core.formula import Variable, Not, Or, Bottom
from proof_helper.core.proof import Statement, Proof, StepID
from proof_helper.logic.rules_custom import CustomRule

def test_match_and_substitute_bottom():
    b1 = Bottom()
    b2 = Bottom()
    subst = {}

    assert b1.match(b2, subst)
    assert b1.substitute(subst) is b1

def test_match_and_substitute_or():
    P = Variable("P")
    Q = Variable("Q")
    A = Variable("A")
    B = Variable("B")

    formula = Or(P, Q)
    pattern = Or(A, B)

    subst = {}
    assert pattern.match(formula, subst)
    assert subst == {"A": P, "B": Q}

    substituted = pattern.substitute(subst)
    assert isinstance(substituted, Or)
    assert substituted.left == P
    assert substituted.right == Q

def test_or_match_fails_on_wrong_type():
    P = Variable("P")
    Q = Variable("Q")
    formula = Or(P, Q)
    different = Not(P)

    pattern = Or(Variable("A"), Variable("B"))
    subst = {}
    assert not pattern.match(different, subst)
