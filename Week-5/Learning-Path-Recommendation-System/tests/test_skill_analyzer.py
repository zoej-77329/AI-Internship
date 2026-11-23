import pytest

from src.skill_analyzer import (
    analyze_skills,
    get_career_requirements,
    identify_uncovered_skills,
    generate_skill_gap_report
)


def test_skill_coverage():

    result = analyze_skills(
        ["Python", "Pandas"],
        ["Python", "Pandas", "Statistics", "SQL"]
    )

    assert result["coverage"] == 50.0
    assert len(result["matched_skills"]) == 2
    assert len(result["missing_skills"]) == 2


def test_skill_normalization():

    result = analyze_skills(
        ["python", "ml"],
        ["Python", "Machine Learning", "Statistics"]
    )

    assert result["matched_skills"] == [
        "Machine Learning",
        "Python"
    ]

    assert result["coverage"] == 66.67


def test_invalid_career():

    with pytest.raises(ValueError, match="Career goal 'Unknown Career' was not found."):
        get_career_requirements("Unknown Career")


def test_uncovered_skills():

    result = identify_uncovered_skills(
        ["Python", "Nonexistent Skill"]
    )

    assert "Nonexistent Skill" in result


def test_complete_report():

    result = generate_skill_gap_report(
        ["Python", "Statistics"],
        "AI Engineer"
    )

    assert result["career_goal"] == "AI Engineer"
    assert "missing_skills" in result
    assert "coverage" in result
