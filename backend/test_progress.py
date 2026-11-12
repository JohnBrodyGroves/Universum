from progress import connect, get_progress, set_stage


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
    