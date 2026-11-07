from content import load_skills
from practice import check_answer, find_question, pick_question

SKILLS = {skill["id"]: skill for skill in load_skills()}

def test_pick_then_find_gives_the_same_question():
    skill = SKILLS["whole-number-operations"]
    for _ in range(50):
        question_id, question = pick_question(skill)
        assert find_question(skill, question_id) == question

def test_written_question_by_id():
    skill = SKILLS["whole-number-operations"]
    assert find_question(skill, "written-1")["answer"] == "84"

def test_bad_ids_give_none():
    skill = SKILLS["whole-number-operations"]
    assert find_question(skill, "written-99") is None
    assert find_question(skill, "nonsense") is None
    assert find_question(skill, "order_of_operations_basic-5") is None

def test_check_numeric_answers():
    question = {"type": "numeric", "answer": "1200"}
    assert check_answer(question, "1200")
    assert check_answer(question, "1,200")
    assert check_answer(question, "1200.0")
    assert not check_answer(question, "1201")
    assert not check_answer(question, "twelve hundred")
    assert not check_answer(question, "")

def test_check_fraction_and_decimal_match():
    question = {"type": "numeric", "answer": "0.75"}
    assert check_answer(question, "3/4")
    assert not check_answer(question, "1/0")

def test_check_choice_answers():
    question = {"type": "choice", "answer": "84", "choices": ["19", "74", "84", "96"]}
    assert check_answer(question, "84")
    assert not check_answer(question, "74")
