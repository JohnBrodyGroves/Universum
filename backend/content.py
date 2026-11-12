from pathlib import Path

import yaml

from generators import GENERATORS

CONTENT_DIR = Path(__file__).parent.parent / "content"
REQUIRED_FIELDS = ["id", "title", "branch", "prerequisites", "questions"]


def load_skills(content_dir=CONTENT_DIR):
    """Read every skill folder (content/<subject>/<skill>/) and stop if any file is broken."""
    skills = []
    for path in sorted(content_dir.rglob("skill.yaml")):
        skill = yaml.safe_load(path.read_text(encoding="utf-8"))
        skill["lesson"] = (path.parent / "lesson.md").read_text(encoding="utf-8")
        skill["path"] = list(path.parent.parent.relative_to(content_dir).parts)
        skills.append(skill)
    errors = validate_skills(skills)
    if errors:
        raise ValueError("Problems in content files:\n" + "\n".join(errors))
    return skills


def validate_skills(skills):
    """Return a list of problems in plain words. An empty list means everything is fine."""
    errors = []
    ids = [skill.get("id") for skill in skills]

    for skill in skills:
        name = skill.get("id", "(skill with no id)")
        for field in REQUIRED_FIELDS:
            if field not in skill:
                errors.append(f"{name}: missing '{field}'")
        if ids.count(skill.get("id")) > 1:
            errors.append(f"{name}: two skills use this id")
        for prereq in skill.get("prerequisites", []):
            if prereq not in ids:
                errors.append(f"{name}: prerequisite '{prereq}' does not exist")
        for generator in skill.get("generators", []):
            if generator not in GENERATORS:
                errors.append(f"{name}: generator '{generator}' does not exist")
        for number, question in enumerate(skill.get("questions", []), start=1):
            for field in ["type", "prompt", "answer", "explanation"]:
                if field not in question:
                    errors.append(f"{name}, question {number}: missing '{field}'")
            if question.get("type") == "choice" and question.get("answer") not in question.get("choices", []):
                errors.append(f"{name}, question {number}: the answer is not one of the choices")

    errors += find_loops(skills)
    return sorted(set(errors))


def find_loops(skills):
    """A skill must never depend on itself, even through other skills (A needs B, B needs A)."""
    prereqs = {skill.get("id"): skill.get("prerequisites", []) for skill in skills}
    errors = []

    def depends_on(start, target, seen):
        for prereq in prereqs.get(start, []):
            if prereq == target:
                return True
            if prereq not in seen:
                seen.add(prereq)
                if depends_on(prereq, target, seen):
                    return True
        return False

    for skill_id in prereqs:
        if depends_on(skill_id, skill_id, set()):
            errors.append(f"{skill_id}: its prerequisites loop back to itself")
    return errors


if __name__ == "__main__":
    load_skills()
    print("All content files look good.")
