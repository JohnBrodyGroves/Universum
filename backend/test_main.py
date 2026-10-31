from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "Ok"} 

def test_skills():
    response = client.get("/api/skills")
    assert response.status_code == 200
    skills = response.json()
    assert len(skills) == 3
    assert skills[0]["id"] == "whole-numbers"
    