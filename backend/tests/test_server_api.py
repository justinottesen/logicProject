import pytest
from proof_helper.server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_verify_syntax(client):
    response = client.post('/api/verify/syntax', json={'statement': 'A → B'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'valid' in data
    assert 'message' in data

def test_verify_step(client):
    response = client.post('/api/verify/step', json={'step': {'statement': 'B', 'rule': 'Modus Ponens', 'support': [0, 1]}})
    assert response.status_code == 200
    data = response.get_json()
    assert 'valid' in data
    assert 'message' in data

def test_verify_proof(client):
    proof = {
        'premises': ['A → B', 'A'],
        'steps': [
            {'statement': 'B', 'rule': 'Modus Ponens', 'support': [0, 1]}
        ],
        'conclusions': ['B']
    }
    response = client.post('/api/verify/proof', json={'proof': proof})
    assert response.status_code == 200
    data = response.get_json()
    assert 'valid' in data
    assert 'message' in data