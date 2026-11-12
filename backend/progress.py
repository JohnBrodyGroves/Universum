import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "universum.db"
PRACTICE_GOAL = 10 # Correct answers in total that finish practice


def connect(db_path=DB_PATH):
    """Open the database file (SQLite creates it the first time) and make sure the table exists."""
    # FastAPI answers requests on several threads, so let them share this connection
    db = sqlite3.connect(db_path, check_same_thread=False)
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS progress (
            learner TEXT NOT NULL,
            skill_id TEXT NOT NULL,
            stage INTEGER NOT NULL,
            correct INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (learner, skill_id)
        )
        """
    )
    return db


def get_progress(db, learner):
    """Every skill this learner has started, as {skill_id: stage}. Missing skills are stage 0."""
    rows = db.execute("SELECT skill_id, stage FROM progress WHERE learner = ?", (learner,))
    return dict(rows.fetchall())


def set_stage(db, learner, skill_id, stage):
    """Save a learner's stage for one skill, adding the row or updating it."""
    with db:  # commits the change, or undoes it if something goes wrong
        db.execute(
            """
            INSERT INTO progress (learner, skill_id, stage) VALUES (?, ?, ?)
            ON CONFLICT (learner, skill_id) DO UPDATE SET stage = excluded.stage
            """,
            (learner, skill_id, stage),
        )

def record_answer(db, learner, skill_id, correct):
    """Count one practice answer and level the learner up. Returns their stage afterwards."""
    with db:
        # Answering at all means the lesson is read: Learn is done, so stage 1
        db.execute(
            """
            INSERT INTO progress (learner, skill_id, stage) VALUES (?, ?, 1)
            ON CONFLICT (learner, skill_id) DO UPDATE SET stage = MAX(stage, 1)
            """,
            (learner, skill_id),
        )
        if correct:
            db.execute(
                "UPDATE progress SET correct = correct + 1 WHERE learner = ? AND skill_id = ?",
                (learner, skill_id),
            )
        stage, total = db.execute(
            "SELECT stage, correct FROM progress WHERE learner = ? AND skill_id = ?",
            (learner, skill_id),
        ).fetchone()
        if stage < 2 and total >= PRACTICE_GOAL:
            stage = 2
            db.execute(
                "UPDATE progress SET stage = 2 WHERE learner = ? AND skill_id = ?",
                (learner, skill_id),
            )
    return stage