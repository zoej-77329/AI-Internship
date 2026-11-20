import pandas as pd

from src.skill_analyzer import generate_skill_gap_report
from src.similarity_engine import recommend_courses
from src.data_loader import load_processed_courses


def get_personalized_recommendations(
    user_skills,
    career_goal,
    top_n=5,
    level=None,
    max_duration=None
):
    # Step 1: Analyze the user's skill gap
    skill_report = generate_skill_gap_report(
        user_skills,
        career_goal
    )

    missing_skills = skill_report["missing_skills"]

    # Step 2: Load cleaned course dataset
    courses = load_processed_courses()

    # Step 3: Apply optional course-level filter
    if level:
        courses = courses[
            courses["level"].str.casefold() == level.casefold()
        ]

    # Step 4: Apply optional duration filter
    if max_duration is not None:
        courses = courses[
            courses["duration_hours"] <= max_duration
        ]

    # Step 5: Generate recommendations
    recommendations = recommend_courses(
        missing_skills=missing_skills,
        top_n=top_n,
        courses=courses
    )

    # Step 6: Generate recommendation reasons
    recommendations["recommendation_reason"] = (
    recommendations["matched_skills"].apply(
           lambda skills: (
            "Covers: " + ", ".join(skills)
            if skills
            else "Related course based on content similarity"
           )
        )
    )
    # Step 7: Return complete results
    return {
        "career_goal": career_goal,
        "skill_report": skill_report,
        "recommendations": recommendations,
        "total_recommendations": len(recommendations),
        "uncovered_skills": skill_report["uncovered_skills"]
    }


if __name__ == "__main__":

    user_skills = [
        "Python",
        "Pandas",
        "SQL"
    ]

    career_goal = "Data Scientist"

    result = get_personalized_recommendations(
        user_skills=user_skills,
        career_goal=career_goal,
        top_n=5
    )

    print("\nCAREER GOAL")
    print("-----------")
    print(result["career_goal"])

    print("\nMISSING SKILLS")
    print("--------------")
    print(result["skill_report"]["missing_skills"])

    print("\nRECOMMENDED COURSES")
    print("-------------------")

    if result["recommendations"].empty:
        print("No matching courses found.")

    else:
        print(
            result["recommendations"][
                [
                    "course_name",
                    "matched_skills",
                    "skill_coverage",
                    "similarity_score",
                    "ranking_score",
                    "recommendation_reason"
                ]
            ].to_string(index=False)
        )

    print("\nSKILLS WITHOUT AVAILABLE COURSES")
    print("--------------------------------")
    print(result["uncovered_skills"])