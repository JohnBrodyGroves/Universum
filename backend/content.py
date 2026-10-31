from pathlib import Path

import yaml

CONTENT_DIR = Path(__file__).parent.parent / "content"


def load_skills(content_dir=CONTENT_DIR):
    """Read every skill folder (content/<subject>/<skill>/) into a list of dicts."""
    skills = []
    for path in sorted(content_dir.glob("*/*/skill.yaml")):
        skill = yaml.safe_load(path.read_text(encoding="utf-8"))
        skill["lesson"] = (path.parent / "lesson.md").read_text(encoding="utf-8")
        skills.append(skill)
    return skills
