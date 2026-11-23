import pandas as pd

from src.similarity_engine import recommend_courses


def sample_courses():
    return pd.DataFrame([
        {
            "course_id": 1,
            "course_name": "Machine Learning with Python",
            "description": "Learn machine learning algorithms and practical Python.",
            "skills": "Python|Machine Learning|Statistics",
            "level": "Intermediate",
            "duration_hours": 20
        },
        {
            "course_id": 2,
            "course_name": "Frontend Development",
            "description": "Build websites using HTML, CSS and JavaScript.",
            "skills": "HTML|CSS|JavaScript",
            "level": "Beginner",
            "duration_hours": 15
        },
        {
            "course_id": 3,
            "course_name": "Python for Data Analysis",
            "description": "Analyze datasets using Python and Pandas.",
            "skills": "Python|Pandas|Data Cleaning",
            "level": "Beginner",
            "duration_hours": 12
        }
    ])


def test_recommendations_are_returned():
    result = recommend_courses(
        ["Python", "Machine Learning"],
        courses=sample_courses()
    )

    assert not result.empty
    assert "Machine Learning with Python" in result["course_name"].values


def test_unrelated_course_is_not_recommended():
    result = recommend_courses(
        ["Machine Learning"],
        courses=sample_courses()
    )

    assert "Frontend Development" not in result["course_name"].values


def test_skill_coverage():
    result = recommend_courses(
        ["Python", "Machine Learning"],
        courses=sample_courses()
    )

    first_course = result.iloc[0]

    assert first_course["skill_coverage"] == 100.0


def test_empty_missing_skills():
    result = recommend_courses(
        [],
        courses=sample_courses()
    )

    assert result.empty


def test_top_n_limit():
    result = recommend_courses(
        ["Python", "Pandas"],
        top_n=1,
        courses=sample_courses()
    )

    assert len(result) <= 1