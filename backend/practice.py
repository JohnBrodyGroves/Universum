"""Pick practice questions and find them again by id, without storing anything."""

import random
from fractions import Fraction

from generators import generate

def pick_question(skill, rng=None):
    """Choose one question for this skill. Returns (question_id, question)."""
    rng = rng or random.Random()
    choices = [f"written-{i}" for i in range(len(skill["questions"]))]
    for name in skill.get("generators", []):
        choices.append(f"{name}-{rng.randint(1, 1_000_000)}")
    question_id = rng.choice(choices)
    return question_id, find_question(skill, question_id)

def find_question(skill, question_id):
    """Rebuild the exact question from its id. Returns None if the id not valid."""
    kind, _, number = question_id.rpartition("-")
    if not number.isdigit():
        return None
    if kind == "written":
        index = int(number)
        if index < len(skill["questions"]):
            return skill["questions"][index]
        return None
    if kind in skill.get("generators", []):
        # The same seed always gives the same random numbers, so the same question will be generated again.
        return generate(kind, random.Random(int(number)))
    return None

def check_answer(question, given):
    """True if the learner's answer is matches. Forgiving about spaces, commas, and number format."""
    given = given.strip().replace(",", "")
    if question["type"] == "choice":
        return given == question["answer"]
    try:
        #Fraction reads "84", "84.0", "-3", "0.75", and "3/4", and compares them exactly
        return Fraction(given) == Fraction(question["answer"])
    except (ValueError, ZeroDivisionError):
        return False
