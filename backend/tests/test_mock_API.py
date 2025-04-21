import pytest
from proof_helper.server import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_verify_valid_conjunction_proof(client):
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
    data = response.get_json()
    assert data["valid"] is True

def test_verify_invalid_proof_wrong_rule(client):
    payload = {
        "premises": [
            {
                "id": "1",
                "formula": { "type": "var", "name": "P" },
                "rule": "Gibberish"
            }
        ],
        "steps": [],
        "conclusions": []
    }

    response = client.post("/verify/proof", json=payload)
    assert response.status_code == 400 or not response.get_json()["valid"]

def test_verify_malformed_json(client):
    response = client.post("/verify/proof", data="not json at all")
    assert response.status_code == 400
    assert "valid" in response.get_json()
    assert response.get_json()["valid"] is False
