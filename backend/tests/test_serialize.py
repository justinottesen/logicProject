import pytest
import json

from proof_helper.core.formula import Variable, Not, And, Or, Bottom
from proof_helper.core.proof import Statement, Subproof, Proof, StepID
from proof_helper.io.serialize import dump_formula, dump_statement, dump_subproof, dump_proof
from proof_helper.io.deserialize import build_proof

def sid(s: str) -> StepID:
    return StepID.from_string(s)

def stmt(id: str, formula, rule=None, premises=None):
    return Statement(id=sid(id), formula=formula, rule=rule, premises=premises or [])

def test_serialize_formula_and_not():
    f = And(Variable("P"), Not(Variable("Q")))
    result = dump_formula(f)
    assert result == {
        "type": "and",
        "left": {"type": "var", "name": "P"},
        "right": {"type": "not", "value": {"type": "var", "name": "Q"}}
    }

def test_serialize_statement():
    f = Or(Variable("A"), Variable("B"))
    s = stmt("1", f, rule="Or Introduction", premises=[sid("2")])
    result = dump_statement(s)

    assert result == {
        "id": "1",
        "formula": {
            "type": "or",
            "left": {"type": "var", "name": "A"},
            "right": {"type": "var", "name": "B"}
        },
        "rule": "Or Introduction",
        "premises": ["2"]
    }

def test_serialize_subproof():
    assume = stmt("1.1", Variable("P"), rule="Assumption")
    inner = stmt("1.2", Bottom(), rule="Bottom Introduction", premises=["1.1", "1.1"])
    sp = Subproof(id=sid("1"), assumption=assume, steps=[inner])

    result = dump_subproof(sp)

    assert result["id"] == "1"
    assert result["type"] == "subproof"
    assert result["assumption"]["formula"]["type"] == "var"
    assert result["steps"][0]["formula"]["type"] == "bottom"

def test_serialize_full_proof():
    P = Variable("P")
    Q = Variable("Q")
    a = stmt("1", P, rule="Assumption")
    b = stmt("2", Q, rule="Assumption")
    ab = stmt("3", And(P, Q), rule="And Introduction", premises=[sid("1"), sid("2")])
    reiterate = stmt("4", And(P, Q), rule="Reiteration", premises=[sid("3")])

    proof = Proof(premises=[a, b], steps=[ab], conclusions=[reiterate])

    result = dump_proof(proof)
    assert "premises" in result
    assert "steps" in result
    assert "conclusions" in result
    assert result["conclusions"][0]["rule"] == "Reiteration"

def test_serialize_roundtrip():
    P = Variable("P")
    Q = Variable("Q")
    a = stmt("1", P, rule="Assumption")
    b = stmt("2", Q, rule="Assumption")
    ab = stmt("3", And(P, Q), rule="And Introduction", premises=[sid("1"), sid("2")])
    reiterate = stmt("4", And(P, Q), rule="Reiteration", premises=[sid("3")])

    original = Proof(premises=[a, b], steps=[ab], conclusions=[reiterate])
    json_data = dump_proof(original)
    json_str = json.dumps(json_data)

    loaded = build_proof(json.loads(json_str))

    assert original.premises[0].formula == loaded.premises[0].formula
    assert original.conclusions[0].formula == loaded.conclusions[0].formula
