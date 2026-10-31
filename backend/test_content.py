from content import load_skills, validate_skills


def make_skill(skill_id, prerequisites=()):
    return {
        "id": skill_id,
        "title": skill_id,
        "branch": "Arithmetic",
        "prerequisites": list(prerequisites),
        "questions": [
            {"type": "numeric", "prompt": "1 + 1", "answer": "2", "explanation": "Add."},
        ],
    }


def test_real_content_is_valid():
    assert len(load_skills()) > 0


def test_good_skills_have_no_errors():
    skills = [make_skill("a"), make_skill("b", ["a"])]
    assert validate_skills(skills) == []


def test_missing_prerequisite_is_caught():
    errors = validate_skills([make_skill("b", ["does-not-exist"])])
    assert errors == ["b: prerequisite 'does-not-exist' does not exist"]


def test_loop_is_caught():
    errors = validate_skills([make_skill("a", ["b"]), make_skill("b", ["a"])])
    assert "a: its prerequisites loop back to itself" in errors


def test_duplicate_id_is_caught():
    errors = validate_skills([make_skill("a"), make_skill("a")])
    assert "a: two skills use this id" in errors


def test_choice_answer_must_be_a_choice():
    skill = make_skill("a")
    skill["questions"] = [
        {"type": "choice", "prompt": "Pick", "choices": ["1", "2"], "answer": "3", "explanation": "x"},
    ]
    assert validate_skills([skill]) == ["a, question 1: the answer is not one of the choices"]


def test_unknown_generator_is_caught():
    skill = make_skill("a")
    skill["generators"] = ["no_such_generator"]
    assert validate_skills([skill]) == ["a: generator 'no_such_generator' does not exist"]
