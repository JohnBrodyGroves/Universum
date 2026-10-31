from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello from Universum!"}


@app.get("/api/health")
def health():
    return {"status": "Ok"}

# shortcut: hard-coded until Phase 2 loads skills from the content/ folder
SKILLS = [
    {"id": "whole-numbers", "title": "Whole numbers", "prerequisites": []},
    {"id": "fractions", "title": "Fractions", "prerequisites": ["whole-numbers"]},
    {"id": "decimals", "title": "Decimals", "prerequisites": ["fractions"]},
]


@app.get("/api/skills")
def skills():
    return SKILLS