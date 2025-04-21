import pytest
from proof_helper.rules import (
    and_elimination_rule,
    or_elimination_rule,
    not_elimination_rule,
    bottom_elimination_rule,
    conditional_elimination_rule,
    biconditional_elimination_rule
)
from proof_helper.formula import Variable, And, Or, Not, Implies, Iff, Bottom
from proof_helper.proof import Statement, StepID, Subproof

# === Helpers ===

def stmt(id: str, formula, rule=None, premises=None):
    return Statement(
        id=StepID.from_string(id),
        formula=formula,
        rule=rule or "∧ Elimination",
        premises=premises or []
    )

def subproof(id: str, assumption: Statement, steps):
    return Subproof(
        id=StepID.from_string(id),
        assumption=assumption,
        steps=steps
    )

def conj(*args):
    """Build left-nested conjunctions from a list of formulas."""
    if len(args) == 1:
        return args[0]
    return And(args[0], conj(*args[1:]))

def disj(*args):
    """Left-nested chain of disjunctions: Or(a, Or(b, Or(...)))"""
    if len(args) == 1:
        return args[0]
    return Or(args[0], disj(*args[1:]))

# === AND ELIMINATION ===

def test_and_elim_single_conjunct():
    P, Q, R = Variable("P"), Variable("Q"), Variable("R")
    support = stmt("1", conj(P, Q, R))
    derived = stmt("2", Q, premises=[StepID.from_string("1")])
    assert and_elimination_rule([support], derived)

def test_and_elim_multi_conjunct_subset():
    P, Q, R, S = Variable("P"), Variable("Q"), Variable("R"), Variable("S")
    support = stmt("1", conj(P, Q, R, S))
    subset = stmt("2", conj(Q, S), premises=[StepID.from_string("1")])
    assert and_elimination_rule([support], subset)

def test_and_elim_all_same_formula():
    P, Q = Variable("P"), Variable("Q")
    support = stmt("1", conj(P, Q))
    derived = stmt("2", conj(Q, P), premises=[StepID.from_string("1")])  # order doesn't matter
    assert and_elimination_rule([support], derived)

def test_and_elim_full_conjunction_same_order():
    P, Q, R = Variable("P"), Variable("Q"), Variable("R")
    support = stmt("1", conj(P, Q, R))
    same = stmt("2", conj(P, Q, R), premises=[StepID.from_string("1")])
    assert and_elimination_rule([support], same)

def test_and_elim_invalid_formula_not_subset():
    P, Q, R = Variable("P"), Variable("Q"), Variable("R")
    support = stmt("1", conj(P, Q))
    not_subset = stmt("2", conj(Q, R), premises=[StepID.from_string("1")])
    assert not and_elimination_rule([support], not_subset)

def test_and_elim_wrong_formula_type():
    P = Variable("P")
    Q = Variable("Q")
    support = stmt("1", P)
    invalid = stmt("2", Q, premises=[StepID.from_string("1")])
    assert not and_elimination_rule([support], invalid)

def test_and_elim_extra_supports_invalid():
    P, Q = Variable("P"), Variable("Q")
    support = stmt("1", conj(P, Q))
    extra = stmt("2", Variable("X"))
    derived = stmt("3", Q, premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert not and_elimination_rule([support, extra], derived)

# === OR ELIMINATION ===

def test_or_elimination_valid():
    P = Variable("P")
    Q = Variable("Q")
    R = Variable("R")

    disj = stmt("1", Or(P, Q))
    case1 = subproof("2", stmt("2.1", P), [stmt("2.2", R)])
    case2 = subproof("3", stmt("3.1", Q), [stmt("3.2", R)])
    result = stmt("4", R, premises=[StepID.from_string("1"), StepID.from_string("2"), StepID.from_string("3")])

    assert or_elimination_rule([disj, case1, case2], result)

def test_or_elimination_valid_reversed_cases():
    P = Variable("P")
    Q = Variable("Q")
    R = Variable("R")

    disj = stmt("1", Or(P, Q))
    case1 = subproof("2", stmt("2.1", Q), [stmt("2.2", R)])
    case2 = subproof("3", stmt("3.1", P), [stmt("3.2", R)])
    result = stmt("4", R, premises=[StepID.from_string("1"), StepID.from_string("2"), StepID.from_string("3")])

    assert or_elimination_rule([disj, case1, case2], result)

def test_or_elimination_wrong_conclusion():
    P = Variable("P")
    Q = Variable("Q")
    R = Variable("R")
    S = Variable("S")

    disj = stmt("1", Or(P, Q))
    case1 = subproof("2", stmt("2.1", P), [stmt("2.2", R)])
    case2 = subproof("3", stmt("3.1", Q), [stmt("3.2", R)])
    result = stmt("4", S, premises=[StepID.from_string("1"), StepID.from_string("2"), StepID.from_string("3")])

    assert not or_elimination_rule([disj, case1, case2], result)

def test_or_elimination_wrong_assumptions():
    P = Variable("P")
    Q = Variable("Q")
    R = Variable("R")

    disj = stmt("1", Or(P, Q))
    case1 = subproof("2", stmt("2.1", R), [stmt("2.2", Q)])  # wrong assumption
    case2 = subproof("3", stmt("3.1", Q), [stmt("3.2", Q)])
    result = stmt("4", Q, premises=[StepID.from_string("1"), StepID.from_string("2"), StepID.from_string("3")])

    assert not or_elimination_rule([disj, case1, case2], result)

def test_or_elimination_wrong_result_mismatch():
    P = Variable("P")
    Q = Variable("Q")
    R = Variable("R")
    S = Variable("S")

    disj = stmt("1", Or(P, Q))
    case1 = subproof("2", stmt("2.1", P), [stmt("2.2", R)])
    case2 = subproof("3", stmt("3.1", Q), [stmt("3.2", S)])
    result = stmt("4", R, premises=[StepID.from_string("1"), StepID.from_string("2"), StepID.from_string("3")])

    assert not or_elimination_rule([disj, case1, case2], result)

def test_or_elimination_too_few_supports():
    disj = stmt("1", Or(Variable("P"), Variable("Q")))
    case1 = subproof("2", stmt("2.1", Variable("P")), [stmt("2.2", Variable("R"))])
    result = stmt("3", Variable("R"), premises=[StepID.from_string("1"), StepID.from_string("2")])

    assert not or_elimination_rule([disj, case1], result)

def test_or_elimination_three_disjuncts():
    P, Q, R = Variable("P"), Variable("Q"), Variable("R")
    X = Variable("X")

    disj_stmt = stmt("1", disj(P, Q, R))

    sp1 = subproof("2", stmt("2.1", P), [stmt("2.2", X)])
    sp2 = subproof("3", stmt("3.1", Q), [stmt("3.2", X)])
    sp3 = subproof("4", stmt("4.1", R), [stmt("4.2", X)])

    conclusion = stmt("5", X, premises=[StepID.from_string("1"), StepID.from_string("2"),
                                        StepID.from_string("3"), StepID.from_string("4")])

    assert or_elimination_rule([disj_stmt, sp1, sp2, sp3], conclusion)

def test_or_elimination_three_disjuncts_one_missing():
    P, Q, R = Variable("P"), Variable("Q"), Variable("R")
    X = Variable("X")

    disj_stmt = stmt("1", disj(P, Q, R))

    sp1 = subproof("2", stmt("2.1", P), [stmt("2.2", X)])
    sp2 = subproof("3", stmt("3.1", Q), [stmt("3.2", X)])
    # missing R

    conclusion = stmt("4", X, premises=[StepID.from_string("1"), StepID.from_string("2"),
                                        StepID.from_string("3")])

    assert not or_elimination_rule([disj_stmt, sp1, sp2], conclusion)

def test_or_elimination_disjunct_handled_twice():
    P, Q = Variable("P"), Variable("Q")
    X = Variable("X")

    disj_stmt = stmt("1", disj(P, Q))

    sp1 = subproof("2", stmt("2.1", P), [stmt("2.2", X)])
    sp2 = subproof("3", stmt("3.1", P), [stmt("3.2", X)])  # duplicate assumption

    conclusion = stmt("4", X, premises=[StepID.from_string("1"), StepID.from_string("2"),
                                        StepID.from_string("3")])

    assert not or_elimination_rule([disj_stmt, sp1, sp2], conclusion)

def test_or_elimination_three_disjuncts_different_conclusions():
    P, Q, R = Variable("P"), Variable("Q"), Variable("R")
    X, Y = Variable("X"), Variable("Y")

    disj_stmt = stmt("1", disj(P, Q, R))

    sp1 = subproof("2", stmt("2.1", P), [stmt("2.2", X)])
    sp2 = subproof("3", stmt("3.1", Q), [stmt("3.2", X)])
    sp3 = subproof("4", stmt("4.1", R), [stmt("4.2", Y)])  # mismatched conclusion

    conclusion = stmt("5", X, premises=[StepID.from_string("1"), StepID.from_string("2"),
                                        StepID.from_string("3"), StepID.from_string("4")])

    assert not or_elimination_rule([disj_stmt, sp1, sp2, sp3], conclusion)

def test_or_elimination_three_disjuncts_out_of_order():
    A, B, C = Variable("A"), Variable("B"), Variable("C")
    Y = Variable("Y")

    disj_stmt = stmt("1", disj(A, B, C))

    sp1 = subproof("2", stmt("2.1", C), [stmt("2.2", Y)])
    sp2 = subproof("3", stmt("3.1", A), [stmt("3.2", Y)])
    sp3 = subproof("4", stmt("4.1", B), [stmt("4.2", Y)])

    conclusion = stmt("5", Y, premises=[StepID.from_string("1"), StepID.from_string("2"),
                                        StepID.from_string("3"), StepID.from_string("4")])

    assert or_elimination_rule([disj_stmt, sp1, sp2, sp3], conclusion)

# === NOT ELIMINATION ===

def test_double_negation_valid():
    P = Variable("P")
    support = stmt("1", Not(Not(P)))
    conclusion = stmt("2", P, premises=[StepID.from_string("1")])
    assert not_elimination_rule([support], conclusion)

def test_double_negation_invalid_formula():
    Q = Variable("Q")
    support = stmt("1", Q)  # not a negation
    conclusion = stmt("2", Q, premises=[StepID.from_string("1")])
    assert not not_elimination_rule([support], conclusion)

def test_double_negation_single_negation():
    Q = Variable("Q")
    support = stmt("1", Not(Q))  # only one negation
    conclusion = stmt("2", Q, premises=[StepID.from_string("1")])
    assert not not_elimination_rule([support], conclusion)

def test_double_negation_mismatched_inner_formula():
    P = Variable("P")
    Q = Variable("Q")
    support = stmt("1", Not(Not(P)))
    conclusion = stmt("2", Q, premises=[StepID.from_string("1")])
    assert not not_elimination_rule([support], conclusion)

def test_double_negation_wrong_number_of_supports():
    P = Variable("P")
    support = stmt("1", Not(Not(P)))
    extra = stmt("2", Variable("Q"))
    conclusion = stmt("3", P, premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert not not_elimination_rule([support, extra], conclusion)

# === BOTTOM ELIMINATION ===

def test_bottom_elim_valid_any_conclusion():
    support = stmt("1", Bottom())
    conclusion = stmt("2", Variable("P"), premises=[StepID.from_string("1")])
    assert bottom_elimination_rule([support], conclusion)

def test_bottom_elim_valid_complex_conclusion():
    A = Variable("A")
    B = Variable("B")
    support = stmt("1", Bottom())
    conclusion = stmt("2", A if hash(A) % 2 == 0 else B, premises=[StepID.from_string("1")])
    assert bottom_elimination_rule([support], conclusion)

def test_bottom_elim_invalid_support_not_bottom():
    support = stmt("1", Variable("P"))
    conclusion = stmt("2", Variable("Q"), premises=[StepID.from_string("1")])
    assert not bottom_elimination_rule([support], conclusion)

def test_bottom_elim_invalid_support_not_statement():
    class FakeStep:
        formula = Bottom()
        id = StepID.from_string("1")

    support = FakeStep()
    conclusion = stmt("2", Variable("X"), premises=[StepID.from_string("1")])
    assert not bottom_elimination_rule([support], conclusion)

def test_bottom_elim_invalid_support_count():
    support1 = stmt("1", Bottom())
    support2 = stmt("2", Bottom())
    conclusion = stmt("3", Variable("Z"), premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert not bottom_elimination_rule([support1, support2], conclusion)

# === CONDITIONAL ELIMINATION ===

def test_conditional_elim_valid_order1():
    P = Variable("P")
    Q = Variable("Q")

    impl = stmt("1", Implies(P, Q))
    premise = stmt("2", P)
    conclusion = stmt("3", Q, premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert conditional_elimination_rule([impl, premise], conclusion)

def test_conditional_elim_valid_order2():
    P = Variable("P")
    Q = Variable("Q")

    impl = stmt("1", Implies(P, Q))
    premise = stmt("2", P)
    conclusion = stmt("3", Q, premises=[StepID.from_string("2"), StepID.from_string("1")])
    assert conditional_elimination_rule([premise, impl], conclusion)

def test_conditional_elim_invalid_mismatched_antecedent():
    P = Variable("P")
    Q = Variable("Q")
    R = Variable("R")

    impl = stmt("1", Implies(R, Q))
    premise = stmt("2", P)
    conclusion = stmt("3", Q, premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert not conditional_elimination_rule([impl, premise], conclusion)

def test_conditional_elim_invalid_mismatched_conclusion():
    P = Variable("P")
    Q = Variable("Q")
    R = Variable("R")

    impl = stmt("1", Implies(P, Q))
    premise = stmt("2", P)
    conclusion = stmt("3", R, premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert not conditional_elimination_rule([impl, premise], conclusion)

def test_conditional_elim_invalid_wrong_number_of_supports():
    P = Variable("P")
    Q = Variable("Q")

    impl = stmt("1", Implies(P, Q))
    conclusion = stmt("2", Q, premises=[StepID.from_string("1")])
    assert not conditional_elimination_rule([impl], conclusion)

# === BICONDITIONAL ELIMINATION ===

def test_biconditional_elim_forward():
    P = Variable("P")
    Q = Variable("Q")
    bicond = stmt("1", Iff(P, Q))
    support = stmt("2", P)
    conclusion = stmt("3", Q, premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert biconditional_elimination_rule([bicond, support], conclusion)

def test_biconditional_elim_backward():
    P = Variable("P")
    Q = Variable("Q")
    bicond = stmt("1", Iff(P, Q))
    support = stmt("2", Q)
    conclusion = stmt("3", P, premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert biconditional_elimination_rule([bicond, support], conclusion)

def test_biconditional_elim_reverse_formula():
    P = Variable("P")
    Q = Variable("Q")
    bicond = stmt("1", Iff(Q, P))
    support = stmt("2", Q)
    conclusion = stmt("3", P, premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert biconditional_elimination_rule([bicond, support], conclusion)

def test_biconditional_elim_support_order_swapped():
    P = Variable("P")
    Q = Variable("Q")
    support = stmt("1", P)
    bicond = stmt("2", Iff(P, Q))
    conclusion = stmt("3", Q, premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert biconditional_elimination_rule([support, bicond], conclusion)

def test_biconditional_elim_invalid_mismatch():
    P = Variable("P")
    Q = Variable("Q")
    R = Variable("R")
    bicond = stmt("1", Iff(P, Q))
    support = stmt("2", R)
    conclusion = stmt("3", Q, premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert not biconditional_elimination_rule([bicond, support], conclusion)

def test_biconditional_elim_invalid_wrong_result():
    P = Variable("P")
    Q = Variable("Q")
    bicond = stmt("1", Iff(P, Q))
    support = stmt("2", P)
    conclusion = stmt("3", Variable("X"), premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert not biconditional_elimination_rule([bicond, support], conclusion)

def test_biconditional_elim_invalid_support_count():
    P = Variable("P")
    Q = Variable("Q")
    bicond = stmt("1", Iff(P, Q))
    conclusion = stmt("2", Q, premises=[StepID.from_string("1")])
    assert not biconditional_elimination_rule([bicond], conclusion)