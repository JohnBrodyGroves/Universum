from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from content import load_skills

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
        }
        for skill in SKILLS
    ]


# Serve the built frontend (after `npm run build`). Must come after the /api routes.
FRONTEND_DIST = Path(__file__).parent.parent / "frontend" / "dist"
if FRONTEND_DIST.is_dir():
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
