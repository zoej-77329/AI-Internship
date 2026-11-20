import pandas as pd

from src.learning_path_generator import generate_learning_path


def test_learning_path_structure():

    result = generate_learning_path(
        user_skills=["Python", "Pandas", "SQL"],
        career_goal="Data Scientist",
        top_n=5
    )

    assert "learning_path" in result
    assert "total_courses" in result
    assert "total_duration" in result
    assert "unresolved_prerequisites" in result


def test_learning_path_step_order():

    result = generate_learning_path(
        user_skills=["Python"],
        career_goal="Data Scientist",
        top_n=5
    )

    path = result["learning_path"]

    if not path.empty:
        assert path["step"].tolist() == list(
            range(1, len(path) + 1)
        )


def test_learning_path_duration():

    result = generate_learning_path(
        user_skills=["Python", "Pandas"],
        career_goal="Data Scientist",
        top_n=5
    )

    path = result["learning_path"]

    expected_duration = (
        path["duration_hours"].sum()
        if not path.empty
        else 0
    )

    assert result["total_duration"] == expected_duration