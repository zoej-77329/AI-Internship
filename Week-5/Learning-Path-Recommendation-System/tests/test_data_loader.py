import pandas as pd
from src.data_loader import (
    load_courses,
    load_career_skills,
    load_processed_courses,
    load_processed_career_skills
)


def test_load_courses():
    df = load_courses()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    expected_cols = ["course_id", "course_name", "skills", "level", "duration_hours"]
    for col in expected_cols:
        assert col in df.columns


def test_load_career_skills():
    df = load_career_skills()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    expected_cols = ["career_goal", "required_skills"]
    for col in expected_cols:
        assert col in df.columns


def test_load_processed_courses():
    df = load_processed_courses()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "course_id" in df.columns
    assert "course_name" in df.columns
    assert "skills" in df.columns
    # course_id should be unique in processed dataset
    assert df["course_id"].is_unique


def test_load_processed_career_skills():
    df = load_processed_career_skills()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "career_goal" in df.columns
    assert "required_skills" in df.columns
    # career_goal should be unique in processed dataset
    assert df["career_goal"].is_unique
