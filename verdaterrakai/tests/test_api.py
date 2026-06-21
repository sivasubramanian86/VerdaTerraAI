from fastapi.testclient import TestClient
from verdaterrakai.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_chat_endpoint():
    payload = {"message": "Test the mesh"}
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "Direct Planner Response to: Test the mesh" in data["response"]
