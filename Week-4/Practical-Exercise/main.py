from data_loader import load_career_skills
from skill_gap import analyze_skill_gap
from course_recommender import recommend_courses
from learning_path import generate_learning_path


def main():

    print("\n===== LEARNING PATH RECOMMENDATION SYSTEM =====")

    user_name = input("\nEnter your name: ")

    user_skills_input = input(
        "Enter your current skills separated by commas: "
    )

    user_skills = {
        skill.strip()
        for skill in user_skills_input.split(",")
        if skill.strip()
    }

    careers = load_career_skills()

    print("\nAvailable Career Goals:")

    for goal in careers["career_goal"]:
        print("-", goal)

    career_goal = input("\nEnter your career goal: ").strip()

    # Skill Gap Analysis
    result = analyze_skill_gap(user_skills, career_goal)

    if result is None:
        return

    missing_skills = result["missing_skills"]

    print("\n===== SKILL GAP ANALYSIS =====")
    print("User:", user_name)
    print("Matched Skills:", result["matched_skills"])
    print("Missing Skills:", missing_skills)
    print("Skill Coverage:", round(result["coverage"], 2), "%")

    if not missing_skills:
        print("\nYou already have all the listed required skills!")
        return

    # Course Recommendations
    print("\n===== RECOMMENDED COURSES =====")

    recommendations = recommend_courses(missing_skills)

    if recommendations.empty:
        print("No relevant courses found.")
    else:
        print(
            recommendations[
                [
                    "course_name",
                    "recommendation_score"
                ]
            ].to_string(index=False)
        )

    # Learning Path
    print("\n===== PERSONALIZED LEARNING PATH =====")

    path, remaining = generate_learning_path(
        user_skills,
        result["required_skills"]
    )

    if path:
        for index, course in enumerate(path, start=1):
            print(f"{index}. {course}")
    else:
        print("No suitable learning path could be generated.")

    if remaining:
        print("\nSkills not covered by available courses:", remaining)
    else:
        print("\nAll required skills are covered by the generated path.")


if __name__ == "__main__":
    main()