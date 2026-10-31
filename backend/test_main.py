from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_skills():
    response = client.get("/api/skills")
    assert response.status_code == 200
    skills = response.json()
    ids = [skill["id"] for skill in skills]
    assert "whole-number-operations" in ids
    assert "order-of-operations" in ids


def test_skills_never_include_answers():
    for skill in client.get("/api/skills").json():
        assert "questions" not in skill
