from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_classify_api_contract_ham():
    response = client.post("/classify", json={"text": "hello"})
    assert response.status_code == 200

    data = response.json()
    assert "label" in data
    assert "score" in data
    assert data["label"] == "ham"
    assert data["score"] == 0


def test_classify_api_contract_spam():
    response = client.post("/classify", json={"text": "free click"})
    assert response.status_code == 200

    data = response.json()
    assert data["label"] == "spam"
    assert data["score"] >= 2


def test_classify_api_empty_text():
    response = client.post("/classify", json={"text": ""})
    assert response.status_code == 200

    data = response.json()
    assert data["label"] == "ham"
    assert data["score"] == 0


def test_classify_api_invalid_body():
    response = client.post("/classify", json={})
    assert response.status_code == 422