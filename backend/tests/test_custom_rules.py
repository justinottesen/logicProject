import os
import shutil
import tempfile
import pytest
from proof_helper.logic.rules_custom import CustomRule
from proof_helper.core.proof import Proof, StepID, Statement
from proof_helper.core.formula import Variable, And
from proof_helper.io.rule_storage import CustomRuleStore
from proof_helper.logic.rule_registry import RuleRegistry
from proof_helper.logic.verify import verify_proof
from proof_helper.io.serialize import dump_proof

def sid(s: str) -> StepID:
    return StepID.from_string(s)

def stmt(id: str, formula, rule=None, premises=None):
    return Statement(id=sid(id), formula=formula, rule=rule, premises=premises or [])

def f_var(name):
    return { "type": "var", "name": name }

def f_and(a, b):
    return { "type": "and", "left": a, "right": b }

@pytest.fixture
def temp_rule_dir():
    path = tempfile.mkdtemp()
    yield path
    shutil.rmtree(path)


def test_custom_rule_and_intro_success():
    P = Variable("P")
    Q = Variable("Q")
    A = stmt("1", P, rule="Assumption")
    B = stmt("2", Q, rule="Assumption")
    AB = stmt("3", And(P, Q), rule="And Introduction", premises=[sid("1"), sid("2")])

    proof = Proof(premises=[A, B], steps=[AB], conclusions=[AB])
    rule = CustomRule("Test ∧ Intro", proof)

    result = rule.verify([A, B], AB)
    assert result is True

def test_custom_rule_wrong_premise_formula():
    P = Variable("P")
    Q = Variable("Q")
    R = Variable("R")
    A = stmt("1", P, rule="Assumption")
    B = stmt("2", Q, rule="Assumption")
    AB = stmt("3", And(P, Q), rule="And Introduction", premises=[sid("1"), sid("2")])

    proof = Proof(premises=[A, B], steps=[AB], conclusions=[AB])
    rule = CustomRule("Test ∧ Intro", proof)

    bad = stmt("0", R, rule="Assumption")
    result = rule.verify([A, bad], AB)
    assert result is False

def test_custom_rule_wrong_conclusion_formula():
    P = Variable("P")
    Q = Variable("Q")
    A = stmt("1", P, rule="Assumption")
    B = stmt("2", Q, rule="Assumption")
    AB = stmt("3", And(P, Q), rule="And Introduction", premises=[sid("1"), sid("2")])
    Wrong = stmt("4", P, rule="Reiteration", premises=[sid("1")])

    proof = Proof(premises=[A, B], steps=[AB], conclusions=[AB])
    rule = CustomRule("Test ∧ Intro", proof)

    result = rule.verify([A, B], Wrong)
    assert result is False

def test_save_and_load_custom_rule(temp_rule_dir):
    store = CustomRuleStore(temp_rule_dir)

    P = Variable("P")
    Q = Variable("Q")

    a = Statement(sid("1"), P, "Assumption")
    b = Statement(sid("2"), Q, "Assumption")
    ab = Statement(sid("3"), And(P, Q), "And Introduction", [sid("1"), sid("2")])
    reiterate = Statement(sid("4"), And(P, Q), "Reiteration", [sid("3")])

    proof = Proof(premises=[a, b], steps=[ab], conclusions=[reiterate])
    store.save_rule("conjunction", dump_proof(proof))

    loaded = store.load_rule("conjunction")

    assert isinstance(loaded, Proof)
    assert len(loaded.premises) == 2
    assert len(loaded.steps) == 1
    assert len(loaded.conclusions) == 1

def test_list_rules(temp_rule_dir):
    store = CustomRuleStore(temp_rule_dir)

    P = Variable("P")
    Q = Variable("Q")

    for name, var in [("r1", P), ("r2", Q)]:
        a = Statement(sid("1"), var, "Assumption")
        c = Statement(sid("2"), var, "Reiteration", [sid("1")])
        proof = Proof(premises=[a], steps=[], conclusions=[c])
        store.save_rule(name, dump_proof(proof))

    rules = store.list_rules()
    assert "r1" in rules
    assert "r2" in rules
    assert isinstance(rules["r1"], Proof)

def test_load_missing_rule_returns_none(temp_rule_dir):
    store = CustomRuleStore(temp_rule_dir)
    assert store.load_rule("no_such_rule") is None

def test_loaded_rule_used_in_verification(temp_rule_dir):
    store = CustomRuleStore(temp_rule_dir)

    P = Variable("P")
    Q = Variable("Q")

    a = Statement(sid("1"), P, "Assumption")
    b = Statement(sid("2"), Q, "Assumption")
    ab = Statement(sid("3"), And(P, Q), "And Introduction", [sid("1"), sid("2")])
    reiterate = Statement(sid("4"), And(P, Q), "Reiteration", [sid("3")])

    rule_proof = Proof(premises=[a, b], steps=[ab], conclusions=[reiterate])
    store.save_rule("and_rule", dump_proof(rule_proof))

    # Use the rule in a new proof
    registry = RuleRegistry(custom_rule_store=store)
    a2 = Statement(sid("1"), P, "Assumption")
    b2 = Statement(sid("2"), Q, "Assumption")
    apply_rule = Statement(sid("3"), And(P, Q), "and_rule", [sid("1"), sid("2")])
    final = Statement(sid("4"), And(P, Q), "Reiteration", [sid("3")])

    proof = Proof(premises=[a2, b2], steps=[apply_rule], conclusions=[final])

    result = verify_proof(proof, registry)
    assert result is True
