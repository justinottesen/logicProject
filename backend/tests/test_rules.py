import pytest
from proof_helper.rules import (
    rule_wrapper,
    assumption_rule,
    and_introduction_rule,
    or_introduction_rule,
    not_introduction_rule,
    bottom_introduction_rule,
    conditional_introduction_rule,
    biconditional_introduction_rule,
)
from proof_helper.formula import Variable, And, Or, Bottom, Not, Implies, Iff
from proof_helper.proof import Statement, StepID, Subproof

# Shortcuts
def stmt(id: str, formula, rule=None, premises=None):
    return Statement(
        id=StepID.from_string(id),
        formula=formula,
        rule=rule,
        premises=premises or []
    )

def subproof(id: str, assumption: Statement, steps):
    return Subproof(
        id=StepID.from_string(id),
        assumption=assumption,
        steps=steps
    )

# === RULE WRAPPER ===

def dummy_rule(supports, statement):
    return True

wrapped = rule_wrapper(dummy_rule)

def dummy_step(id_str: str, formula=None):
    return Statement(
        id=StepID.from_string(id_str),
        formula=formula or Variable("X"),
        rule="Dummy",
        premises=[]
    )

def test_rule_passes_all_checks():
    s1 = dummy_step("1")
    s2 = Statement(
        id=StepID.from_string("2"),
        formula=Variable("A"),
        rule="Dummy",
        premises=[StepID.from_string("1")]
    )
    print(s1, s2)
    assert wrapped([s1], s2)

def test_fails_on_missing_rule():
    s1 = dummy_step("1")
    s2 = Statement(
        id=StepID.from_string("2"),
        formula=Variable("A"),
        rule=None,
        premises=[StepID.from_string("1")]
    )
    assert not wrapped([s1], s2)

def test_fails_if_support_not_before_statement():
    s1 = dummy_step("3")  # After statement
    s2 = Statement(
        id=StepID.from_string("2"),
        formula=Variable("A"),
        rule="Dummy",
        premises=[StepID.from_string("3")]
    )
    assert not wrapped([s1], s2)

def test_fails_if_supports_do_not_match_premises():
    s1 = dummy_step("1")
    s2 = Statement(
        id=StepID.from_string("2"),
        formula=Variable("A"),
        rule="Dummy",
        premises=[StepID.from_string("99")]  # Wrong ID
    )
    assert not wrapped([s1], s2)

def test_fails_if_statement_is_wrong_type():
    class NotAStatement:
        id = StepID.from_string("2")
        rule = "Dummy"
        premises = []

    s1 = dummy_step("1")
    fake = NotAStatement()
    assert not wrapped([s1], fake)

# === ASSUMPTION ===

def test_assumption_valid():
    s = stmt("1", Variable("P"), rule="Assumption", premises=[])
    assert assumption_rule([], s)

def test_assumption_with_supports_fails():
    support = stmt("1", Variable("P"))
    s = stmt("2", Variable("P"), rule="Assumption", premises=[StepID.from_string("1")])
    assert not assumption_rule([support], s)

# === AND INTRODUCTION ===

def test_and_intro_valid():
    a = stmt("1", Variable("P"))
    b = stmt("2", Variable("Q"))
    ab = stmt("3", And(a.formula, b.formula), rule="∧ Introduction", premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert and_introduction_rule([a, b], ab)

def test_and_intro_wrong_formula():
    a = stmt("1", Variable("P"))
    b = stmt("2", Variable("Q"))
    bad = stmt("3", Variable("R"), rule="∧ Introduction", premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert not and_introduction_rule([a, b], bad)

def test_and_intro_missing_conjunct():
    a = stmt("1", Variable("P"))
    b = stmt("2", Variable("Q"))
    ab = stmt("3", And(a.formula, Variable("X")), rule="∧ Introduction", premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert not and_introduction_rule([a, b], ab)

def test_and_intro_nested_clause():
    a = stmt("1", Variable("P"))
    b = stmt("2", Or(Variable("Q"), Variable("R")))
    ab = stmt("3", And(a.formula, b.formula), rule="∧ Introduction", premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert and_introduction_rule([a, b], ab)

# === OR INTRODUCTION ===

def test_or_intro_simple_or():
    support = stmt("1", Variable("P"))
    conclusion = stmt("2", Or(support.formula, Variable("Q")), premises=[StepID.from_string("1")])
    assert or_introduction_rule([support], conclusion)

def test_or_intro_support_is_right_side():
    support = stmt("1", Variable("Q"))
    conclusion = stmt("2", Or(Variable("P"), support.formula), premises=[StepID.from_string("1")])
    assert or_introduction_rule([support], conclusion)

def test_or_intro_nested_valid():
    support = stmt("1", Variable("P"))
    disj = Or(Variable("X"), Or(support.formula, Variable("Y")))
    conclusion = stmt("2", disj, premises=[StepID.from_string("1")])
    assert or_introduction_rule([support], conclusion)

def test_or_intro_deep_buried_invalid():
    support = stmt("1", Variable("P"))
    buried = Or(Variable("X"), Or(Variable("Y"), And(support.formula, Variable("Z"))))  # P is not a disjunct
    conclusion = stmt("2", buried, premises=[StepID.from_string("1")])
    assert not or_introduction_rule([support], conclusion)

def test_or_intro_support_formula_mismatch():
    support = stmt("1", Variable("P"))
    conclusion = stmt("2", Or(Variable("Q"), Variable("R")), premises=[StepID.from_string("1")])
    assert not or_introduction_rule([support], conclusion)

def test_or_intro_multiple_supports_rejected():
    a = stmt("1", Variable("P"))
    b = stmt("2", Variable("Q"))
    conclusion = stmt("3", Or(a.formula, b.formula), premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert not or_introduction_rule([a, b], conclusion)

# === NOT INTRODUCTION ===

def test_not_intro_valid():
    assumption = stmt("1.1", Variable("P"), rule="Assumption")
    contradiction = stmt("1.2", Bottom(), rule="¬E", premises=[StepID.from_string("1.1")])
    sp = subproof("1", assumption, [contradiction])

    conclusion = stmt("2", Not(assumption.formula), rule="¬ Introduction", premises=[StepID.from_string("1")])
    assert not_introduction_rule([sp], conclusion)

def test_not_intro_fails_with_no_bottom():
    assumption = stmt("1.1", Variable("P"), rule="Assumption")
    unrelated = stmt("1.2", Variable("Q"), rule="Assumption")
    sp = subproof("1", assumption, [unrelated])

    conclusion = stmt("2", Not(assumption.formula), rule="¬ Introduction", premises=[StepID.from_string("1")])
    assert not not_introduction_rule([sp], conclusion)

def test_not_intro_wrong_conclusion():
    assumption = stmt("1.1", Variable("P"), rule="Assumption")
    contradiction = stmt("1.2", Bottom(), rule="¬E", premises=[StepID.from_string("1.1")])
    sp = subproof("1", assumption, [contradiction])

    wrong_conclusion = stmt("2", Variable("Q"), rule="¬ Introduction", premises=[StepID.from_string("1")])
    assert not not_introduction_rule([sp], wrong_conclusion)

def test_not_intro_wrong_assumption():
    assumption = stmt("1.1", Variable("Q"), rule="Assumption")  # should be P
    contradiction = stmt("1.2", Bottom(), rule="¬E", premises=[StepID.from_string("1.1")])
    sp = subproof("1", assumption, [contradiction])

    conclusion = stmt("2", Not(Variable("P")), rule="¬ Introduction", premises=[StepID.from_string("1")])
    assert not not_introduction_rule([sp], conclusion)

def test_not_intro_support_is_not_subproof():
    fake_support = stmt("1", Variable("P"), rule="¬E")
    conclusion = stmt("2", Not(Variable("P")), rule="¬ Introduction", premises=[StepID.from_string("1")])
    assert not not_introduction_rule([fake_support], conclusion)

def test_not_intro_multiple_supports_invalid():
    a = stmt("1", Variable("P"))
    b = stmt("2", Variable("Q"))
    conclusion = stmt("3", Not(Variable("R")), rule="¬ Introduction", premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert not not_introduction_rule([a, b], conclusion)

# === BOTTOM INTRODUCTION ===

def test_bottom_intro_valid():
    p = Variable("P")
    a = stmt("1", p)
    b = stmt("2", Not(p))
    bottom = stmt("3", Bottom(), premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert bottom_introduction_rule([a, b], bottom)

def test_bottom_intro_valid_reversed():
    p = Variable("P")
    a = stmt("1", Not(p))
    b = stmt("2", p)
    bottom = stmt("3", Bottom(), premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert bottom_introduction_rule([a, b], bottom)

def test_bottom_intro_fails_wrong_formula():
    p = Variable("P")
    a = stmt("1", p)
    b = stmt("2", Not(p))
    not_bottom = stmt("3", Variable("Q"), premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert not bottom_introduction_rule([a, b], not_bottom)

def test_bottom_intro_fails_if_not_negation():
    a = stmt("1", Variable("P"))
    b = stmt("2", Variable("Q"))
    bottom = stmt("3", Bottom(), premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert not bottom_introduction_rule([a, b], bottom)

def test_bottom_intro_fails_if_not_statements():
    class NotAStatement:
        formula = Variable("P")
        id = StepID.from_string("1")
    a = NotAStatement()
    b = stmt("2", Not(Variable("P")))
    bottom = stmt("3", Bottom(), premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert not bottom_introduction_rule([a, b], bottom)

def test_bottom_intro_wrong_number_of_supports():
    a = stmt("1", Variable("P"))
    bottom = stmt("2", Bottom(), premises=[StepID.from_string("1")])
    assert not bottom_introduction_rule([a], bottom)

# === CONDITIONAL INTRODUCTION TESTS ===

def test_conditional_intro_valid():
    p = Variable("P")
    q = Variable("Q")

    assume = stmt("1.1", p)
    conclusion = stmt("1.2", q)
    sp = subproof("1", assume, [conclusion])

    outer = stmt("2", Implies(p, q), rule="→ Introduction", premises=[StepID.from_string("1")])
    assert conditional_introduction_rule([sp], outer)

def test_conditional_intro_empty_subproof():
    assume = stmt("1.1", Variable("P"))
    sp = subproof("1", assume, [])

    outer = stmt("2", Implies(assume.formula, Variable("Q")), rule="→ Introduction", premises=[StepID.from_string("1")])
    assert not conditional_introduction_rule([sp], outer)

def test_conditional_intro_subproof_does_not_end_with_statement():
    class FakeStep:
        formula = Variable("Q")
        id = StepID.from_string("1.2")
    assume = stmt("1.1", Variable("P"))
    sp = subproof("1", assume, [FakeStep()])

    outer = stmt("2", Implies(assume.formula, Variable("Q")), rule="→ Introduction", premises=[StepID.from_string("1")])
    assert not conditional_introduction_rule([sp], outer)

def test_conditional_intro_wrong_formula():
    p = Variable("P")
    q = Variable("Q")

    assume = stmt("1.1", p)
    conclusion = stmt("1.2", q)
    sp = subproof("1", assume, [conclusion])

    wrong = stmt("2", Variable("X"), rule="→ Introduction", premises=[StepID.from_string("1")])
    assert not conditional_introduction_rule([sp], wrong)

def test_conditional_intro_not_subproof():
    p = Variable("P")
    q = Variable("Q")

    fake_support = stmt("1", p)
    conclusion = stmt("2", Implies(p, q), rule="→ Introduction", premises=[StepID.from_string("1")])
    assert not conditional_introduction_rule([fake_support], conclusion)

def test_conditional_intro_too_many_supports():
    a = stmt("1", Variable("P"))
    b = stmt("2", Variable("Q"))
    outer = stmt("3", Implies(a.formula, b.formula), rule="→ Introduction", premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert not conditional_introduction_rule([a, b], outer)

# === BICONDITIONAL INTRODUCTION TESTS ===

def test_biconditional_intro_valid():
    p = Variable("P")
    q = Variable("Q")

    sp1 = subproof("1", stmt("1.1", p), [stmt("1.2", q)])
    sp2 = subproof("2", stmt("2.1", q), [stmt("2.2", p)])

    conclusion = stmt("3", Iff(p, q), rule="↔ Introduction", premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert biconditional_introduction_rule([sp1, sp2], conclusion)

def test_biconditional_intro_valid_reversed():
    p = Variable("P")
    q = Variable("Q")

    sp1 = subproof("1", stmt("1.1", q), [stmt("1.2", p)])
    sp2 = subproof("2", stmt("2.1", p), [stmt("2.2", q)])

    conclusion = stmt("3", Iff(q, p), rule="↔ Introduction", premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert biconditional_introduction_rule([sp1, sp2], conclusion)

def test_biconditional_intro_mismatched_formula():
    p = Variable("P")
    q = Variable("Q")
    r = Variable("R")

    sp1 = subproof("1", stmt("1.1", p), [stmt("1.2", q)])
    sp2 = subproof("2", stmt("2.1", q), [stmt("2.2", p)])

    wrong = stmt("3", Iff(p, r), rule="↔ Introduction", premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert not biconditional_introduction_rule([sp1, sp2], wrong)

def test_biconditional_intro_invalid_structure():
    # No conclusion in subproof
    p = Variable("P")
    q = Variable("Q")

    sp1 = subproof("1", stmt("1.1", p), [])
    sp2 = subproof("2", stmt("2.1", q), [stmt("2.2", p)])

    conclusion = stmt("3", Iff(p, q), rule="↔ Introduction", premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert not biconditional_introduction_rule([sp1, sp2], conclusion)

def test_biconditional_intro_wrong_support_types():
    a = stmt("1", Variable("P"))
    b = stmt("2", Variable("Q"))
    conclusion = stmt("3", Iff(a.formula, b.formula), rule="↔ Introduction", premises=[StepID.from_string("1"), StepID.from_string("2")])
    assert not biconditional_introduction_rule([a, b], conclusion)

def test_biconditional_intro_wrong_number_of_supports():
    p = Variable("P")
    q = Variable("Q")
    sp1 = subproof("1", stmt("1.1", p), [stmt("1.2", q)])
    conclusion = stmt("2", Iff(p, q), rule="↔ Introduction", premises=[StepID.from_string("1")])
    assert not biconditional_introduction_rule([sp1], conclusion)