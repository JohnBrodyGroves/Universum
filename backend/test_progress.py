from progress import connect, get_progress, set_stage, record_answer


def test_new_learner_has_no_progress():
    db = connect(":memory:")
    assert get_progress(db, "ana") == {}


def test_set_and_update_stage():
    db = connect(":memory:")
    set_stage(db, "ana", "negative-numbers", 1)
    set_stage(db, "ana", "negative-numbers", 3)
    set_stage(db, "ben", "negative-numbers", 5)
    assert get_progress(db, "ana") == {"negative-numbers": 3}
    assert get_progress(db, "ben") == {"negative-numbers": 5}

def test_first_answer_finishes_learn():
    db = connect(":memory:")
    assert record_answer(db, "ana", "negative-numbers", False) == 1


def test_ten_correct_in_total_finishes_practice():
    db = connect(":memory:")
    for _ in range(9):
        assert record_answer(db, "ana", "negative-numbers", True) == 1
    assert record_answer(db, "ana", "negative-numbers", False) == 1  # mistakes don't reset the count
    assert record_answer(db, "ana", "negative-numbers", True) == 2
    assert get_progress(db, "ana") == {"negative-numbers": 2}


def test_never_moves_a_learner_down():
    db = connect(":memory:")
    set_stage(db, "ana", "negative-numbers", 4)
    assert record_answer(db, "ana", "negative-numbers", False) == 4