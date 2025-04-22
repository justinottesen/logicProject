import pytest
from proof_helper.core.formula import Variable, Not, And, Or, Implies, Iff, Bottom
from proof_helper.logic.formula_similarity import score_similarity

P = Variable("P")
Q = Variable("Q")
R = Variable("R")

def test_identical_variables():
    assert score_similarity(P, Variable("P")) == 1.0

def test_different_variables():
    assert score_similarity(P, Q) == 0.0

def test_identical_bottom():
    assert score_similarity(Bottom(), Bottom()) == 1.0

def test_not_same_variable():
    assert score_similarity(Not(P), Not(P)) == pytest.approx(0.9)

def test_not_different_variable():
    assert score_similarity(Not(P), Not(Q)) == 0.0

def test_and_same_order():
    assert score_similarity(And(P, Q), And(P, Q)) == pytest.approx(0.9)

def test_and_reverse_order():
    assert score_similarity(And(P, Q), And(Q, P)) == pytest.approx(0.9)

def test_and_vs_or():
    assert score_similarity(And(P, Q), Or(P, Q)) == 0.0

def test_and_with_partial_match():
    assert score_similarity(And(P, Q), And(P, R)) < 0.9

def test_implies_identical():
    assert score_similarity(Implies(P, Q), Implies(P, Q)) == pytest.approx(0.9)

def test_iff_vs_implies():
    assert score_similarity(Iff(P, Q), Implies(P, Q)) == 0.0
