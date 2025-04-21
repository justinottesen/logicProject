import pytest
from proof_helper.rules import (
    rule_wrapper,
    assumption_rule,
    and_introduction_rule,
)
from proof_helper.formula import Variable, And, Or
from proof_helper.proof import Statement, StepID

# Shortcuts
def stmt(id: str, formula, rule=None, premises=None):
    return Statement(
        id=StepID.from_string(id),
        formula=formula,
        rule=rule,
        premises=premises or []
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
