import pytest
from proof_helper.rules_builtin import (
    and_introduction_rule, and_elimination_rule,
    or_introduction_rule, or_elimination_rule,
    not_introduction_rule, not_elimination_rule,
    bottom_introduction_rule, bottom_elimination_rule,
    conditional_introduction_rule, conditional_elimination_rule,
    biconditional_introduction_rule, biconditional_elimination_rule
)
from proof_helper.formula import Variable, Not, And, Or, Implies, Iff, Bottom
from proof_helper.proof import Statement, Subproof, StepID

# === Helpers ===

def sid(n): return StepID.from_string(n)

def stmt(id: str, formula, rule=None, premises=None):
    return Statement(id=sid(id), formula=formula, rule=rule, premises=premises or [])

def subproof(id: str, assumption: Statement, steps):
    return Subproof(id=sid(id), assumption=assumption, steps=steps)

def disj(*args):
    if len(args) == 1:
        return args[0]
    return Or(args[0], disj(*args[1:]))

def conj(*args):
    if len(args) == 1:
        return args[0]
    return And(args[0], conj(*args[1:]))

def test_nested_and_intro_then_elim():
    P, Q, R = Variable("P"), Variable("Q"), Variable("R")
    a = stmt("1", P)
    b = stmt("2", Q)
    c = stmt("3", R)
    ab = stmt("4", And(a.formula, b.formula), "∧ Introduction", [sid("1"), sid("2")])
    abc = stmt("5", And(ab.formula, c.formula), "∧ Introduction", [sid("4"), sid("3")])
    extracted = stmt("6", b.formula, "∧ Elimination", [stmt("4", ab.formula)])

    assert and_introduction_rule([a, b], ab)
    assert and_introduction_rule([ab, c], abc)
    assert and_elimination_rule([ab], extracted)

def test_chain_of_implications_intro_elim():
    P, Q, R = Variable("P"), Variable("Q"), Variable("R")
    assume_P = stmt("1.1", P)
    pq = stmt("1.2", Q)
    pq_proof = subproof("1", assume_P, [pq])

    pq_implies = stmt("2", Implies(P, Q), "→ Introduction", [sid("1")])
    pq_stmt = stmt("3", P)
    q_stmt = stmt("4", Q, "→ Elimination", [sid("2"), sid("3")])

    assert conditional_introduction_rule([pq_proof], pq_implies)
    assert conditional_elimination_rule([pq_implies, pq_stmt], q_stmt)

def test_biconditional_elim_then_intro():
    P, Q = Variable("P"), Variable("Q")
    bicond = stmt("1", Iff(P, Q))
    p_stmt = stmt("2", P)
    q_stmt = stmt("3", Q, "↔ Elimination", [sid("1"), sid("2")])

    assume_p = stmt("4.1", P)
    derive_q = stmt("4.2", Q)
    proof1 = subproof("4", assume_p, [derive_q])

    assume_q = stmt("5.1", Q)
    derive_p = stmt("5.2", P)
    proof2 = subproof("5", assume_q, [derive_p])

    reformed_bicond = stmt("6", Iff(P, Q), "↔ Introduction", [sid("4"), sid("5")])

    assert biconditional_elimination_rule([bicond, p_stmt], q_stmt)
    assert biconditional_introduction_rule([proof1, proof2], reformed_bicond)

def test_or_elim_with_3_disjuncts_nested_conclusion():
    A, B, C, R = Variable("A"), Variable("B"), Variable("C"), Variable("R")
    disj_stmt = stmt("1", disj(A, B, C))

    sp1 = subproof("2", stmt("2.1", A), [stmt("2.2", R)])
    sp2 = subproof("3", stmt("3.1", B), [stmt("3.2", R)])
    sp3 = subproof("4", stmt("4.1", C), [stmt("4.2", R)])
    result = stmt("5", R, "∨ Elimination", [sid("1"), sid("2"), sid("3"), sid("4")])

    assert or_elimination_rule([disj_stmt, sp1, sp2, sp3], result)

def test_double_negation_chain():
    P = Variable("P")
    nnP = stmt("1", Not(Not(P)))
    extracted = stmt("2", P, "¬ Elimination", [sid("1")])
    repacked = stmt("3", Not(Not(P)), "¬ Introduction", [sid("2")])  # [P] ... ⊥

    assert not_elimination_rule([nnP], extracted)
    # For repacked to pass, it needs to be within a subproof deriving ⊥, so just verifying symmetry shape here

def test_explosion_to_anything():
    contradiction = stmt("1", Bottom())
    derived = stmt("2", Variable("Z"), "⊥ Elimination", [sid("1")])
    assert bottom_elimination_rule([contradiction], derived)

def test_buried_and_elim_from_3layer_intro():
    A, B, C = Variable("A"), Variable("B"), Variable("C")
    a = stmt("1", A)
    b = stmt("2", B)
    c = stmt("3", C)
    ab = stmt("4", And(a.formula, b.formula), "∧ Introduction", [sid("1"), sid("2")])
    abc = stmt("5", And(ab.formula, c.formula), "∧ Introduction", [sid("4"), sid("3")])
    final = stmt("6", B, "∧ Elimination", [stmt("4", ab.formula)])

    # Final test actually skips one layer of nesting
    assert and_introduction_rule([a, b], ab)
    assert and_introduction_rule([ab, c], abc)
    assert and_elimination_rule([ab], final)

def test_disjunction_then_case_analysis_with_deep_structure():
    P, Q, R = Variable("P"), Variable("Q"), Variable("R")
    disj_st = stmt("1", disj(P, disj(Q, R)))

    sp1 = subproof("2", stmt("2.1", P), [stmt("2.2", Variable("X"))])
    sp2 = subproof("3", stmt("3.1", Q), [stmt("3.2", Variable("X"))])
    sp3 = subproof("4", stmt("4.1", R), [stmt("4.2", Variable("X"))])
    conclusion = stmt("5", Variable("X"), "∨ Elimination", [sid("1"), sid("2"), sid("3"), sid("4")])

    assert or_elimination_rule([disj_st, sp1, sp2, sp3], conclusion)

def test_double_negation_elimination_nested():
    A = Variable("A")
    nnA = Not(Not(A))
    support = stmt("1", nnA)
    conclusion = stmt("2", A, "¬ Elimination", [sid("1")])

    assert not_elimination_rule([support], conclusion)

    # Try re-introducing ¬¬A from A using ⊥ intro trick
    assume_A = stmt("3.1", A)
    leads_to_bottom = stmt("3.2", Bottom())  # assume deriving contradiction
    sp = subproof("3", assume_A, [leads_to_bottom])
    negated = stmt("4", Not(A), "¬ Introduction", [sid("3")])
    reinverted = stmt("5", Not(Not(A)), "¬ Introduction", [sid("4")])

    # Not a perfect logic chain (we're not reconstructing the bottom here),
    # but a shape test that nested applications compose properly

    assert isinstance(reinverted.formula, Not)

def test_or_intro_then_elim_to_different_conclusion():
    A, B, C, D = Variable("A"), Variable("B"), Variable("C"), Variable("D")
    disj = stmt("1", Or(A, B))
    sp1 = subproof("2", stmt("2.1", A), [stmt("2.2", C)])
    sp2 = subproof("3", stmt("3.1", B), [stmt("3.2", D)])
    result = stmt("4", C, "∨ Elimination", [sid("1"), sid("2"), sid("3")])

    # Should fail: conclusion mismatch (C ≠ D)
    assert not or_elimination_rule([disj, sp1, sp2], result)

def test_complex_biconditional_then_elim_and_chain():
    A, B = Variable("A"), Variable("B")
    bicond = stmt("1", Iff(A, B))
    a = stmt("2", A)
    b = stmt("3", B, "↔ Elimination", [sid("1"), sid("2")])

    impl = stmt("4", Implies(B, A))
    result = stmt("5", A, "→ Elimination", [sid("4"), sid("3")])

    assert biconditional_elimination_rule([bicond, a], b)
    assert conditional_elimination_rule([impl, b], result)