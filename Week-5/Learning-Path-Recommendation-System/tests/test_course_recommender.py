import pandas as pd

from src.course_recommender import get_personalized_recommendations


def test_recommendation_result_structure():
    result = get_personalized_recommendations(
        user_skills=["Python", "Pandas", "SQL"],
        career_goal="Data Scientist",
        top_n=5
    )

    assert "career_goal" in result
    assert "skill_report" in result
    assert "recommendations" in result
    assert "uncovered_skills" in result


def test_recommendation_limit():
    result = get_personalized_recommendations(
        user_skills=["Python"],
        career_goal="Data Scientist",
        top_n=2
    )

    assert len(result["recommendations"]) <= 2


def test_recommendation_columns():
    result = get_personalized_recommendations(
        user_skills=["Python"],
        career_goal="Data Scientist"
    )

    expected_columns = [
        "course_name",
        "matched_skills",
        "skill_coverage",
        "similarity_score",
        "ranking_score",
        "recommendation_reason"
    ]

    for column in expected_columns:
        assert column in result["recommendations"].columns