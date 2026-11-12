from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from content import load_skills
from practice import check_answer, find_question, pick_question
from progress import connect, get_progress, record_answer

app = FastAPI()


@app.get("/api/health")
def health():
    return {"status": "ok"}


SKILLS = load_skills()

@app.get("/api/skills")
def skills():
    # Only the summary: never send answers to the browser
    return [
        {
            "id": skill["id"],
            "title": skill["title"],
            "branch": skill["branch"],
            "prerequisites": skill["prerequisites"],
            "path": skill["path"],
        }
        for skill in SKILLS
    ]

def get_skill(skill_id):
    for skill in SKILLS:
        if skill["id"] == skill_id:
            return skill
    raise HTTPException(status_code=404, detail="No skill with that id")

@app.get("/api/skills/{skill_id}")
def one_skill(skill_id: str):
    skill = get_skill(skill_id)
    return {"id": skill["id"], "title": skill["title"], "lesson": skill["lesson"]}

@app.get("/api/skills/{skill_id}/question")
def question(skill_id: str):
    question_id, question = pick_question(get_skill(skill_id))
    #Everything except the answer and explanation
    return {
        "question_id": question_id,
        "type": question["type"],
        "prompt": question["prompt"],
        "choices": question.get("choices"),
    }

class Answer(BaseModel):
    question_id: str
    answer: str

@app.post("/api/skills/{skill_id}/answer")
def answer(skill_id: str, body: Answer):
    question = find_question(get_skill(skill_id), body.question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="No question with that id")
    correct = check_answer(question, body.answer)
    stage = record_answer(DB, LEARNER, skill_id, correct)
    if correct:
        return {"correct": True, "stage": stage}
    #No hints: say what went wrong and which skill to work on
    return {"correct": False, "explanation": question["explanation"], "skill": skill_id, "stage": stage}

DB = connect()
LEARNER = "me" #shortcut: one learner until name + Pin login exists

@app.get("/api/progress")
def learner_progress():
    return get_progress(DB, LEARNER)

# Serve the built frontend (after `npm run build`). Must come after the /api routes.
FRONTEND_DIST = Path(__file__).parent.parent / "frontend" / "dist"
if FRONTEND_DIST.is_dir():
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
