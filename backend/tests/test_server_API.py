import tempfile
import shutil
import pytest
from proof_helper.app.server import ProofApp, register_routes
import json

@pytest.fixture
def client():
    tempdir = tempfile.mkdtemp()
    app = ProofApp(__name__, rules_dir=tempdir)
    register_routes(app)
    app.testing = True
    with app.test_client() as client:
        yield client
    shutil.rmtree(tempdir)

def f_var(name):
    return { "type": "var", "name": name }

def f_and(a, b):
    return { "type": "and", "left": a, "right": b }

def f_or(left, right):
    return { "type": "or", "left": left, "right": right }

def test_valid_proof_returns_200(client):
    payload = {
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
                "rule": "And Introduction",
                "premises": ["1", "2"]
            }
        ],
        "conclusions": [
            {
                "id": "4",
                "formula": {
                    "type": "and",
                    "left": { "type": "var", "name": "P" },
                    "right": { "type": "var", "name": "Q" }
                },
                "rule": "Reiteration",
                "premises": ["3"]
            }
        ]
    }

    response = client.post("/verify_proof", json=payload)
    assert response.status_code == 200
    assert response.data == b""
    
def test_missing_rule_returns_400(client):
    payload = {
        "premises": [
            {
                "id": "1",
                "formula": { "type": "var", "name": "P" }
                # missing rule
            }
        ],
        "steps": [],
        "conclusions": []
    }

    response = client.post("/verify_proof", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["step_id"] == "1"
    assert "Premise must use rule 'Assumption'" in data["message"]

def test_conclusion_references_missing_step(client):
    payload = {
        "premises": [
            {
                "id": "1",
                "formula": { "type": "var", "name": "P" },
                "rule": "Assumption"
            }
        ],
        "steps": [],
        "conclusions": [
            {
                "id": "2",
                "formula": { "type": "var", "name": "P" },
                "rule": "Reiteration",
                "premises": ["999"]
            }
        ]
    }

    response = client.post("/verify_proof", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["step_id"] == "2"
    assert "not found" in data["message"]

def test_malformed_json_returns_400(client):
    response = client.post("/verify_proof", data="not valid json")
    assert response.status_code == 400
    data = response.get_json()
    assert "step_id" in data
    assert data["step_id"] is None

def test_verify_proof_valid(client):
    payload = {
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
    response = client.post("/verify_proof", json=payload)
    assert response.status_code == 200

def test_verify_proof_invalid_rule(client):
    payload = {
        "premises": [
            {"id": "1", "formula": f_var("P")}
        ],
        "steps": [],
        "conclusions": []
    }
    response = client.post("/verify_proof", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "step_id" in data

def test_post_rules_valid(client):
    rule = {
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
    response = client.post("/rules", json={
        "name": "AndRule",
        "proof": rule
    })
    assert response.status_code == 200

def test_post_rules_invalid(client):
    bad_rule = {
        "premises": [
            {"id": "1", "formula": f_var("P")}
        ],
        "steps": [],
        "conclusions": []
    }
    response = client.post("/rules", json={
        "name": "BadRule",
        "proof": bad_rule
    })
    assert response.status_code == 400
    assert "step_id" in response.get_json()

def test_uploaded_rule_used_in_proof(client):
    # First upload the custom rule
    rule = {
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
    upload = client.post("/rules", json={"name": "AndCustom", "proof": rule})
    assert upload.status_code == 200

    # Now verify a proof using the custom rule
    proof = {
        "premises": [
            {"id": "1", "formula": f_var("P"), "rule": "Assumption"},
            {"id": "2", "formula": f_var("Q"), "rule": "Assumption"}
        ],
        "steps": [
            {"id": "3", "formula": f_and(f_var("P"), f_var("Q")), "rule": "AndCustom", "premises": ["1", "2"]}
        ],
        "conclusions": [
            {"id": "4", "formula": f_and(f_var("P"), f_var("Q")), "rule": "Reiteration", "premises": ["3"]}
        ]
    }
    verify = client.post("/verify_proof", json=proof)
    assert verify.status_code == 200

def test_get_rules_returns_builtin_and_custom(client):
    # Post a valid custom rule
    rule = {
        "premises": [
            {"id": "1", "formula": {"type": "var", "name": "P"}, "rule": "Assumption"},
            {"id": "2", "formula": {"type": "var", "name": "Q"}, "rule": "Assumption"}
        ],
        "steps": [
            {
                "id": "3",
                "formula": {
                    "type": "and",
                    "left": {"type": "var", "name": "P"},
                    "right": {"type": "var", "name": "Q"}
                },
                "rule": "And Introduction",
                "premises": ["1", "2"]
            }
        ],
        "conclusions": [
            {
                "id": "4",
                "formula": {
                    "type": "and",
                    "left": {"type": "var", "name": "P"},
                    "right": {"type": "var", "name": "Q"}
                },
                "rule": "Reiteration",
                "premises": ["3"]
            }
        ]
    }

    upload = client.post("/rules", json={"name": "TestConjunction", "proof": rule})
    assert upload.status_code == 200

    # Now query the rules list
    response = client.get("/rules")
    assert response.status_code == 200
    data = response.get_json()
    assert "builtin" in data
    assert "custom" in data
    assert "TestConjunction" in data["custom"]
    assert "And Introduction" in data["builtin"]

def test_suggest_rules_basic(client):
    payload = {
        "proof": {
            "premises": [
                {"id": "1", "formula": f_var("P"), "rule": "Assumption"},
                {"id": "2", "formula": f_var("Q"), "rule": "Assumption"}
            ],
            "steps": [],
            "conclusions": [
                {"id": "3", "formula": f_and(f_var("P"), f_var("Q")), "rule": "Reiteration", "premises": ["4"]}
            ]
        },
        "max": 5
    }

    response = client.post("/suggest_rules", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(item["rule"] == "And Introduction" for item in data)
    assert all("formula" in item and "rule" in item and "score" in item for item in data)

def test_suggest_rules_with_custom_max(client):
    payload = {
        "proof": {
            "premises": [{"id": "1", "formula": f_var("P"), "rule": "Assumption"}],
            "steps": [],
            "conclusions": [{"id": "2", "formula": f_or(f_var("P"), f_var("Q")), "rule": "Reiteration", "premises": ["3"]}]
        },
        "max": 1
    }
    response = client.post("/suggest_rules", json=payload)
    assert response.status_code == 200
    assert len(response.get_json()) <= 1

def test_suggest_rules_invalid_max(client):
    payload = {
        "proof": {
            "premises": [],
            "steps": [],
            "conclusions": []
        },
        "max": "not_a_number"
    }
    response = client.post("/suggest_rules", json=payload)
    assert response.status_code == 400

def test_suggest_rules_malformed_json(client):
    response = client.post("/suggest_rules", data="not json")
    assert response.status_code == 400
