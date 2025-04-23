import pytest
import tempfile
import shutil
from proof_helper.logic.step_suggestions import generate_next_steps
from proof_helper.core.formula import Variable, And, Implies, Not, Bottom, Or
from proof_helper.core.proof import Proof, Statement, StepID, Subproof
from proof_helper.logic.rule_registry import RuleRegistry
from proof_helper.io.rule_storage import CustomRuleStore

def sid(s: str) -> StepID:
    return StepID.from_string(s)

def stmt(id_str: str, formula, rule: str = None, premises: list[str] = None):
    return Statement(
        id=sid(id_str),
        formula=formula,
        rule=rule,
        premises=[sid(p) for p in premises] if premises else []
    )

def test_suggestion_and_intro():
    P = Variable("P")
    Q = Variable("Q")

    proof = Proof(
        premises=[
            stmt("1", P, "Assumption"),
            stmt("2", Q, "Assumption"),
        ],
        steps=[],
        conclusions=[
            stmt("3", And(P, Q), "Reiteration", ["4"])
        ]
    )
    registry = RuleRegistry()
    suggestions = generate_next_steps(proof, registry)

    assert any(
        s.formula == And(P, Q) and s.rule == "And Introduction"
        for s, score in suggestions
    )

def test_suggestion_implies_intro():
    P = Variable("P")
    Q = Variable("Q")

    sub = Subproof(
        id=StepID.from_string("1"),
        assumption=stmt("1.1", P, "Assumption"),
        steps=[
            stmt("1.2", Q, "Assumption")
        ]
    )

    proof = Proof(
        premises=[],
        steps=[sub],
        conclusions=[
            stmt("2", Implies(P, Q), "Reiteration", ["3"])
        ]
    )

    registry = RuleRegistry()
    suggestions = generate_next_steps(proof, registry)

    assert any(
        s.formula == Implies(P, Q) and s.rule == "Implication Introduction"
        for s, score in suggestions
    )

def test_suggestion_or_intro():
    P = Variable("P")
    Q = Variable("Q")
    proof = Proof(
        premises=[stmt("1", P, "Assumption")],
        steps=[],
        conclusions=[stmt("2", Or(P, Q), "Reiteration", ["3"])]
    )
    registry = RuleRegistry()
    suggestions = generate_next_steps(proof, registry)
    assert any(s.formula == Or(P, Q) and s.rule == "Or Introduction" for s, _ in suggestions)

def test_suggestion_not_intro():
    P = Variable("P")
    sub = Subproof(
        id=sid("1"),
        assumption=stmt("1.1", P, "Assumption"),
        steps=[
            stmt("1.2", Bottom(), "Bottom Introduction", ["1.1", "1.1"])
        ]
    )
    proof = Proof(
        premises=[],
        steps=[sub],
        conclusions=[stmt("2", Not(P), "Reiteration", ["3"])]
    )
    registry = RuleRegistry()
    suggestions = generate_next_steps(proof, registry)
    assert any(s.formula == Not(P) and s.rule == "Not Introduction" for s, _ in suggestions)

def test_suggestion_bottom_intro():
    P = Variable("P")
    not_P = Not(P)
    proof = Proof(
        premises=[stmt("1", P, "Assumption"), stmt("2", not_P, "Assumption")],
        steps=[],
        conclusions=[stmt("3", Bottom(), "Reiteration", ["4"])]
    )
    registry = RuleRegistry()
    suggestions = generate_next_steps(proof, registry)
    assert any(isinstance(s.formula, Bottom) and s.rule == "Bottom Introduction" for s, _ in suggestions)

def test_suggestion_double_negation_elim():
    P = Variable("P")
    not_not_P = Not(Not(P))
    proof = Proof(
        premises=[stmt("1", not_not_P, "Assumption")],
        steps=[],
        conclusions=[stmt("2", P, "Reiteration", ["3"])]
    )
    registry = RuleRegistry()
    suggestions = generate_next_steps(proof, registry)
    assert any(s.formula == P and s.rule == "Not Elimination" for s, _ in suggestions)

def test_or_intro_single_disjunct_goal():
    P = Variable("P")
    Q = Variable("Q")
    proof = Proof(
        premises=[stmt("1", P, "Assumption")],
        steps=[],
        conclusions=[stmt("2", Or(P, Q), "Reiteration", ["3"])]
    )
    registry = RuleRegistry()
    suggestions = generate_next_steps(proof, registry)
    assert any(s.formula == Or(P, Q) and s.rule == "Or Introduction" for s, _ in suggestions)

def test_or_intro_nested_disjunction_goal():
    P, Q, R = Variable("P"), Variable("Q"), Variable("R")
    proof = Proof(
        premises=[stmt("1", P, "Assumption")],
        steps=[],
        conclusions=[stmt("2", Or(Or(P, Q), R), "Reiteration", ["3"])]
    )
    registry = RuleRegistry()
    suggestions = generate_next_steps(proof, registry)
    assert any(s.formula == Or(Or(P, Q), R) and s.rule == "Or Introduction" for s, _ in suggestions)

def test_or_intro_multiple_possible_disjuncts():
    P, Q = Variable("P"), Variable("Q")
    proof = Proof(
        premises=[stmt("1", P, "Assumption"), stmt("2", Q, "Assumption")],
        steps=[],
        conclusions=[stmt("3", Or(Q, P), "Reiteration", ["4"])]
    )
    registry = RuleRegistry()
    suggestions = generate_next_steps(proof, registry)
    assert any(s.formula == Or(Q, P) and s.rule == "Or Introduction" for s, _ in suggestions)

def test_or_intro_no_goal_generates_default_or():
    P = Variable("P")
    proof = Proof(
        premises=[stmt("1", P, "Assumption")],
        steps=[],
        conclusions=[]
    )
    registry = RuleRegistry()
    suggestions = generate_next_steps(proof, registry)
    assert any(s.formula == Or(P, P) and s.rule == "Or Introduction" for s, _ in suggestions)

def f_var(name):
    return { "type": "var", "name": name }

def f_and(a, b):
    return { "type": "and", "left": a, "right": b }

@pytest.fixture
def temp_rule_dir():
    path = tempfile.mkdtemp()
    yield path
    shutil.rmtree(path)

def test_custom_rule_suggestion():
    P = Variable("P")
    Q = Variable("Q")
    conjunction = And(P, Q)

    # Construct and upload a custom rule
    custom_rule = {
        "premises": [
            {"id": "1", "formula": f_var("P"), "rule": "Assumption"},
            {"id": "2", "formula": f_var("Q"), "rule": "Assumption"}
        ],
        "steps": [
            {"id": "3", "formula": f_and(f_var("P"), f_var("Q")), "rule": "And Introduction", "premises": ["1", "2"]}
        ],
        "conclusions": [
            {"id": "4", "formula": f_and(f_var("P"), f_var("Q")), "rule": "Reiteration", "premises": ["3"]}
        ]
    }

    # Create a registry with the rule loaded
    rule_store = CustomRuleStore(tempfile.mkdtemp())
    rule_store.save_rule("AndCombo", custom_rule)
    registry = RuleRegistry(custom_rule_store=rule_store)

    # Use the rule in a new proof
    proof = Proof(
        premises=[
            stmt("1", P, "Assumption"),
            stmt("2", Q, "Assumption")
        ],
        steps=[],
        conclusions=[stmt("3", conjunction, "Reiteration", ["4"])]
    )

    suggestions = generate_next_steps(proof, registry)
    assert any(
        s.formula == conjunction and s.rule == "AndCombo"
        for s, _ in suggestions
    )
