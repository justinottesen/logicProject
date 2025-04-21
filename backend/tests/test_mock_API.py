import pytest
from proof_helper.server import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

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
                "rule": "∧ Introduction",
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

    response = client.post("/verify/proof", json=payload)
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

    response = client.post("/verify/proof", json=payload)
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

    response = client.post("/verify/proof", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["step_id"] == "2"
    assert "not found" in data["message"]

def test_malformed_json_returns_400(client):
    response = client.post("/verify/proof", data="not valid json")
    assert response.status_code == 400
    data = response.get_json()
    assert "step_id" in data
    assert data["step_id"] is None
