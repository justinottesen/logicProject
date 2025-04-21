import pytest
from proof_helper.io.deserialize import build_proof
from proof_helper.core.formula import Variable, Bottom, Not, And
from proof_helper.core.proof import StepID, Proof, Statement, Subproof

def test_parse_simple_statement():
    json_data = {
        "premises": [
            {
                "id": "1",
                "formula": { "type": "var", "name": "P" },
                "rule": "Assumption"
            }
        ],
        "steps": [],
        "conclusions": []
    }

    proof = build_proof(json_data)
    assert isinstance(proof, Proof)
    assert len(proof.premises) == 1
    stmt = proof.premises[0]
    assert isinstance(stmt, Statement)
    assert stmt.id == StepID.from_string("1")
    assert isinstance(stmt.formula, Variable)
    assert stmt.formula.name == "P"
    assert stmt.rule == "Assumption"

def test_parse_subproof_with_bottom_intro():
    json_data = {
        "premises": [
            {
                "id": "1",
                "formula": { "type": "not", "value": { "type": "var", "name": "P" } },
                "rule": "Assumption"
            }
        ],
        "steps": [
            {
                "id": "2",
                "type": "subproof",
                "assumption": {
                    "id": "2.1",
                    "formula": { "type": "var", "name": "P" },
                    "rule": "Assumption"
                },
                "steps": [
                    {
                        "id": "2.2",
                        "formula": { "type": "bottom" },
                        "rule": "⊥ Introduction",
                        "premises": ["1", "2.1"]
                    }
                ]
            },
            {
                "id": "3",
                "formula": {
                    "type": "or",
                    "left": { "type": "var", "name": "P" },
                    "right": {
                    "type": "not",
                    "value": { "type": "var", "name": "P" }
                    }
                },
                "rule": "¬ Elimination",
                "premises": ["2"]
            }
        ],
        "conclusions": [
            {
                "id": "4",
                "formula": {
                    "type": "or",
                    "left": { "type": "var", "name": "P" },
                    "right": {
                    "type": "not",
                    "value": { "type": "var", "name": "P" }
                    }
                },
                "rule": "Reiteration",
                "premises": ["3"]
            }
        ]
    }

    proof = build_proof(json_data)

    assert isinstance(proof, Proof)
    assert len(proof.premises) == 1
    assert len(proof.steps) == 2
    assert len(proof.conclusions) == 1

    sp = proof.steps[0]
    assert isinstance(sp, Subproof)
    assert sp.assumption.id == StepID.from_string("2.1")
    assert sp.steps[0].id == StepID.from_string("2.2")
    assert isinstance(sp.steps[0].formula, Bottom)

    conclusion = proof.conclusions[0]
    assert conclusion.rule == "Reiteration"
    assert conclusion.premises == [StepID.from_string("3")]

def test_parse_and_formula():
    json_data = {
        "premises": [
            {
                "id": "1",
                "formula": { "type": "var", "name": "P" },
                "rule": "Assumption"
            },
            {
                "id": "2",
                "formula": { "type": "var", "name": "Q" },
                "rule": "Assumption"
            }
        ],
        "steps": [
            {
                "id": "3",
                "formula": {
                    "type": "and",
                    "left": { "type": "var", "name": "P" },
                    "right": { "type": "var", "name": "Q" }
                },
                "rule": "∧ Introduction",
                "premises": ["1", "2"]
            }
        ],
        "conclusions": []
    }

    proof = build_proof(json_data)
    step = proof.steps[0]
    assert isinstance(step.formula, And)
    assert isinstance(step.formula.left, Variable)
    assert step.formula.left.name == "P"
    assert isinstance(step.formula.right, Variable)
    assert step.formula.right.name == "Q"
