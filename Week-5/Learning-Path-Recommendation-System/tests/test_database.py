import sqlite3
import pytest
import pandas as pd
from pathlib import Path

from src.database import (
    init_db,
    get_connection,
    create_profile,
    update_profile,
    get_profile,
    save_profile,
    validate_profile_data,
    mark_course_complete,
    mark_course_incomplete,
    get_completed_courses,
    get_course_progress,
    calculate_progress,
    DatabaseError
)


@pytest.fixture
def temp_db(tmp_path):
    """Provides a path to an isolated temporary SQLite database."""
    db_file = tmp_path / "test_pathfinder.db"
    return db_file


def test_database_initialization(temp_db):
    """Test that database and tables are created safely."""
    assert not temp_db.exists()
    init_db(temp_db)
    assert temp_db.exists()

    with get_connection(temp_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = {row["name"] for row in cursor.fetchall()}
        assert "user_profiles" in tables
        assert "learning_progress" in tables

    # Second init should be idempotent and not raise errors
    init_db(temp_db)


def test_profile_creation_and_retrieval(temp_db):
    """Test creating a profile and retrieving it."""
    profile = create_profile(
        full_name="Alice Developer",
        career_goal="Data Scientist",
        current_skills=["Python", "Pandas", "SQL"],
        experience_level="Intermediate",
        db_path=temp_db
    )

    assert profile is not None
    assert profile["user_id"] == 1
    assert profile["full_name"] == "Alice Developer"
    assert profile["name"] == "Alice Developer"
    assert profile["career_goal"] == "Data Scientist"
    assert profile["current_skills"] == ["Python", "Pandas", "SQL"]
    assert profile["experience_level"] == "Intermediate"
    assert "created_at" in profile
    assert "updated_at" in profile

    # Retrieve by user_id
    retrieved = get_profile(user_id=1, db_path=temp_db)
    assert retrieved is not None
    assert retrieved["full_name"] == "Alice Developer"
    assert retrieved["current_skills"] == ["Python", "Pandas", "SQL"]

    # Retrieve default/latest
    latest = get_profile(db_path=temp_db)
    assert latest is not None
    assert latest["user_id"] == 1


def test_profile_update(temp_db):
    """Test updating an existing profile."""
    created = create_profile(
        full_name="Bob Engineer",
        career_goal="Frontend Developer",
        current_skills=["HTML", "CSS"],
        experience_level="Beginner",
        db_path=temp_db
    )

    updated = update_profile(
        user_id=created["user_id"],
        full_name="Bob Senior Engineer",
        career_goal="Full Stack Developer",
        current_skills=["HTML", "CSS", "JavaScript", "React"],
        experience_level="Advanced",
        db_path=temp_db
    )

    assert updated["full_name"] == "Bob Senior Engineer"
    assert updated["career_goal"] == "Full Stack Developer"
    assert updated["current_skills"] == ["HTML", "CSS", "JavaScript", "React"]
    assert updated["experience_level"] == "Advanced"
    assert updated["created_at"] == created["created_at"]


def test_save_profile_helper(temp_db):
    """Test save_profile auto-creates then updates."""
    # First save creates profile
    p1 = save_profile(
        full_name="Carol Analyst",
        career_goal="Data Analyst",
        current_skills=["SQL", "Excel"],
        experience_level="Beginner",
        db_path=temp_db
    )
    assert p1["user_id"] == 1

    # Second save with same user updates existing
    p2 = save_profile(
        full_name="Carol Senior Analyst",
        career_goal="Data Analyst",
        current_skills=["SQL", "Python", "Tableau"],
        experience_level="Intermediate",
        user_id=1,
        db_path=temp_db
    )
    assert p2["user_id"] == 1
    assert p2["full_name"] == "Carol Senior Analyst"
    assert p2["current_skills"] == ["SQL", "Python", "Tableau"]


def test_profile_validation():
    """Test required field validations."""
    with pytest.raises(ValueError, match="Full name is required"):
        validate_profile_data("", "Data Scientist", "Beginner")

    with pytest.raises(ValueError, match="Career goal is required"):
        validate_profile_data("Alice", "", "Beginner")

    with pytest.raises(ValueError, match="Invalid experience level"):
        validate_profile_data("Alice", "Data Scientist", "Expert")


def test_course_completion_and_progress_retrieval(temp_db):
    """Test marking courses complete and incomplete."""
    user_id = 1

    # Initially empty
    completed = get_completed_courses(user_id=user_id, db_path=temp_db)
    assert completed == set()

    # Mark course 1 and 2 as complete
    mark_course_complete(course_id=1, user_id=user_id, db_path=temp_db)
    mark_course_complete(course_id=2, user_id=user_id, db_path=temp_db)

    completed = get_completed_courses(user_id=user_id, db_path=temp_db)
    assert completed == {1, 2}

    # Verify progress detail
    detail = get_course_progress(user_id=user_id, db_path=temp_db)
    assert 1 in detail
    assert detail[1]["completed"] is True
    assert detail[1]["completion_date"] is not None

    # Mark course 1 as incomplete
    mark_course_incomplete(course_id=1, user_id=user_id, db_path=temp_db)
    completed = get_completed_courses(user_id=user_id, db_path=temp_db)
    assert completed == {2}

    detail = get_course_progress(user_id=user_id, db_path=temp_db)
    assert detail[1]["completed"] is False
    assert detail[1]["completion_date"] is None


def test_calculate_progress(temp_db):
    """Test progress summary calculations."""
    user_id = 1
    mark_course_complete(course_id=101, user_id=user_id, db_path=temp_db)
    mark_course_complete(course_id=102, user_id=user_id, db_path=temp_db)

    mock_path = pd.DataFrame([
        {"course_id": 101, "course_name": "Course 1", "duration_hours": 10},
        {"course_id": 102, "course_name": "Course 2", "duration_hours": 15},
        {"course_id": 103, "course_name": "Course 3", "duration_hours": 20},
        {"course_id": 104, "course_name": "Course 4", "duration_hours": 5},
    ])

    summary = calculate_progress(mock_path, user_id=user_id, db_path=temp_db)
    assert summary["total_courses"] == 4
    assert summary["completed_courses"] == 2
    assert summary["remaining_courses"] == 2
    assert summary["completion_percentage"] == 50.0
    assert summary["total_duration"] == 50.0
    assert summary["completed_hours"] == 25.0
    assert summary["remaining_hours"] == 25.0


def test_persistence_after_reopening_connection(temp_db):
    """Test that data persists across separate database connections."""
    create_profile(
        full_name="David Persistent",
        career_goal="AI Engineer",
        current_skills=["Python", "TensorFlow"],
        experience_level="Intermediate",
        db_path=temp_db
    )
    mark_course_complete(course_id=5, user_id=1, db_path=temp_db)

    # Completely new connection to the same file
    with get_connection(temp_db) as conn2:
        cursor = conn2.cursor()
        cursor.execute("SELECT full_name FROM user_profiles WHERE user_id = 1;")
        row = cursor.fetchone()
        assert row["full_name"] == "David Persistent"

    retrieved_completed = get_completed_courses(user_id=1, db_path=temp_db)
    assert 5 in retrieved_completed
