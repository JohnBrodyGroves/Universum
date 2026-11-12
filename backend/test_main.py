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

def test_one_skill_has_lesson():
    response = client.get("/api/skills/whole-number-operations")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Whole number operations"
    assert "four operations" in data["lesson"]
    assert "questions" not in data
    
def test_unknown_skill_is_404():
    response = client.get("/api/skills/not-a-skill")
    assert response.status_code == 404

def test_question_never_includes_answer():
    for _ in range(20):
        data = client.get("/api/skills/whole-number-operations/question").json()
        assert data["prompt"]
        assert "answer" not in data
        assert "explanation" not in data

def test_answer_right_and_wrong():
    url = "/api/skills/whole-number-operations/answer"
    right = client.post(url, json={"question_id": "written-1", "answer": "84"})
    assert right.json() == {"correct": True}
    wrong = client.post(url, json={"question_id": "written-1", "answer": "19"})
    assert wrong.json()["correct"] is False
    assert "multiply" in wrong.json()["explanation"]

def test_answer_with_bad_question_id_is_404():
    url = "/api/skills/whole-number-operations/answer"
    response = client.post(url, json={"question_id": "nonsense", "answer": "1"})
    assert response.status_code == 404

def test_skills_have_path():
    skills = {s["id"]: s for s in client.get("/api/skills").json()}
    assert skills["whole-number-operations"]["path"] == ["mathematics", "arithmetic"]

def test_progress_is_a_dict():
    response = client.get("/api/progress")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    