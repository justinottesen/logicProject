import pytest
from proof_helper.core.formula import *
from proof_helper.io.parse_formula import parse_formula

def v(name): return Variable(name)

# === Basic parsing ===

def test_single_variable():
    assert parse_formula("P") == v("P")

def test_bottom():
    assert parse_formula("⊥") == Bottom()

def test_not():
    assert parse_formula("¬P") == Not(v("P"))

def test_and():
    assert parse_formula("P ∧ Q") == And(v("P"), v("Q"))

def test_or():
    assert parse_formula("P ∨ Q") == Or(v("P"), v("Q"))

def test_implies():
    assert parse_formula("P → Q") == Implies(v("P"), v("Q"))

def test_iff():
    assert parse_formula("P ↔ Q") == Iff(v("P"), v("Q"))

# === Precedence ===

def test_and_binds_tighter_than_or():
    f = parse_formula("P ∨ Q ∧ R")
    assert f == Or(v("P"), And(v("Q"), v("R")))

def test_nested_not_and_implies():
    f = parse_formula("¬(P → Q)")
    assert f == Not(Implies(v("P"), v("Q")))

def test_full_precedence_chain():
    f = parse_formula("P ↔ Q → R ∨ S ∧ ¬T")
    assert isinstance(f, Iff)
    assert isinstance(f.right, Implies)

def test_grouping_parentheses():
    f = parse_formula("(P ∧ Q) → (¬R ∨ S)")
    assert f == Implies(
        And(v("P"), v("Q")),
        Or(Not(v("R")), v("S"))
    )

# === Complex combinations ===

def test_nested_parens_and_operators():
    f = parse_formula("((¬P ∧ Q) → R) ↔ S")
    assert f == Iff(
        Implies(And(Not(v("P")), v("Q")), v("R")),
        v("S")
    )

# === Error handling ===

def test_missing_paren_raises():
    with pytest.raises(SyntaxError):
        parse_formula("(P ∧ Q")

def test_invalid_token_raises():
    with pytest.raises(SyntaxError):
        parse_formula("P ? Q")

def test_empty_input_raises():
    with pytest.raises(SyntaxError):
        parse_formula("")
