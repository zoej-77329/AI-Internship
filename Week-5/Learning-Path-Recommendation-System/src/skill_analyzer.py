from src.data_loader import (
    load_processed_courses,
    load_processed_career_skills
)
from src.utils import normalize_skill_list

def get_career_requirements(career_goal):

    careers = load_processed_career_skills()

    career = careers[
        careers["career_goal"].str.casefold()
        == career_goal.strip().casefold()
    ]

    if career.empty:
        raise ValueError(
            f"Career goal '{career_goal}' was not found."
        )

    required_skills = career.iloc[0]["required_skills"]

    return normalize_skill_list(required_skills.split("|"))

def analyze_skills(user_skills, required_skills):

    user_skills = set(normalize_skill_list(user_skills))
    required_skills = set(normalize_skill_list(required_skills))

    matched_skills = user_skills.intersection(required_skills)

    missing_skills = required_skills - user_skills

    extra_skills = user_skills - required_skills

    if required_skills:
        coverage = (
            len(matched_skills) / len(required_skills)
        ) * 100
    else:
        coverage = 100.0

    return {
        "user_skills": sorted(user_skills),
        "required_skills": sorted(required_skills),
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "extra_skills": sorted(extra_skills),
        "coverage": round(coverage, 2)
    }

def identify_uncovered_skills(missing_skills):

    courses = load_processed_courses()

    available_skills = set()

    for skills in courses["skills"]:

        available_skills.update(
            normalize_skill_list(skills.split("|"))
        )

    uncovered_skills = (
        set(missing_skills) - available_skills
    )

    return sorted(uncovered_skills)

def generate_skill_gap_report(user_skills, career_goal):

    required_skills = get_career_requirements(career_goal)

    analysis = analyze_skills(
        user_skills,
        required_skills
    )

    uncovered_skills = identify_uncovered_skills(
        analysis["missing_skills"]
    )

    analysis["uncovered_skills"] = uncovered_skills

    analysis["covered_missing_skills"] = sorted(
        set(analysis["missing_skills"]) - set(uncovered_skills)
    )

    analysis["career_goal"] = career_goal

    return analysis