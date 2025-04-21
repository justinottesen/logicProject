from proof_helper.rules import rule_wrapper
from proof_helper.formula import Variable
from proof_helper.proof import Statement, StepID

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