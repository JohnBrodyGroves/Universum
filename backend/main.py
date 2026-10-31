from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()


@app.get("/api/health")
def health():
    return {"status": "fine"}


# shortcut: hard-coded until Phase 2 loads skills from the content/ folder
SKILLS = [
    {"id": "whole-numbers", "title": "Whole numbers", "prerequisites": []},
    {"id": "fractions", "title": "Fractions", "prerequisites": ["whole-numbers"]},
    {"id": "decimals", "title": "Decimals", "prerequisites": ["fractions"]},
]


@app.get("/api/skills")
def skills():
    return SKILLS


# Serve the built frontend (after `npm run build`). Must come after the /api routes.
FRONTEND_DIST = Path(__file__).parent.parent / "frontend" / "dist"
if FRONTEND_DIST.is_dir():
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
    