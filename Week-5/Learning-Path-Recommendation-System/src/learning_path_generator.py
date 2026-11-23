import pandas as pd

from src.data_loader import load_processed_courses
from src.utils import normalize_skill_list
from src.course_recommender import get_personalized_recommendations
from src.similarity_engine import recommend_courses


def split_skills(value):
    if pd.isna(value) or not str(value).strip():
        return []

    return normalize_skill_list(str(value).split("|"))


def generate_learning_path(user_skills, career_goal, top_n=5):

    user_skills = normalize_skill_list(user_skills)

    courses = load_processed_courses()

    result = get_personalized_recommendations(
        user_skills=user_skills,
        career_goal=career_goal,
        top_n=top_n
    )

    recommended_courses = result["recommendations"]

    learning_path = []
    mastered_skills = set(skill.casefold() for skill in user_skills)
    added_courses = set()
    visiting_courses = set()
    unresolved_prerequisites = []

    def add_course(course_id):

        if course_id in added_courses:
            return True

        if course_id in visiting_courses:
            return False

        matching_rows = courses[
            courses["course_id"] == course_id
        ]

        if matching_rows.empty:
            return False

        course = matching_rows.iloc[0]

        visiting_courses.add(course_id)

        prerequisites = split_skills(
            course.get("prerequisites", "")
        )

        # Complete prerequisites before this course
        for prerequisite in prerequisites:

            if prerequisite.casefold() in mastered_skills:
                continue

            prerequisite_courses = recommend_courses(
                missing_skills=[prerequisite],
                top_n=len(courses),
                courses=courses[
                    courses["course_id"] != course_id
                ]
            )

            # Only accept courses that explicitly teach
            # the required prerequisite skill
            matching_prerequisite_courses = (
                prerequisite_courses[
                    prerequisite_courses["matched_skills"].apply(
                        lambda skills: any(
                            skill.casefold() == prerequisite.casefold()
                            for skill in skills
                        )
                    )
                ]
            )

            if matching_prerequisite_courses.empty:

                unresolved_prerequisites.append({
                    "course": course["course_name"],
                    "missing_prerequisite": prerequisite
                })

                visiting_courses.remove(course_id)
                return False

            prerequisite_course_id = (
                matching_prerequisite_courses.iloc[0]["course_id"]
            )

            success = add_course(prerequisite_course_id)

            if not success:

                unresolved_prerequisites.append({
                    "course": course["course_name"],
                    "missing_prerequisite": prerequisite
                })

                visiting_courses.remove(course_id)
                return False

        # Add course after its prerequisites
        if course_id not in added_courses:

            learning_path.append({
                "course_id": course["course_id"],
                "course_name": course["course_name"],
                "level": course["level"],
                "duration_hours": course["duration_hours"],
                "skills": split_skills(course["skills"]),
                "prerequisites": prerequisites
            })

            added_courses.add(course_id)

            # Project assumption: completing a course
            # means the learner acquires its listed skills
            mastered_skills.update(
                skill.casefold()
                for skill in split_skills(course["skills"])
            )

        visiting_courses.remove(course_id)

        return True

    # Add recommended target courses in ranking order
    for _, recommended in recommended_courses.iterrows():

        add_course(recommended["course_id"])

    path_df = pd.DataFrame(learning_path)

    if not path_df.empty:

        path_df.insert(
            0,
            "step",
            range(1, len(path_df) + 1)
        )

        path_df["cumulative_duration"] = (
            path_df["duration_hours"].cumsum()
        )

    total_duration = (
        path_df["duration_hours"].sum()
        if not path_df.empty
        else 0
    )

    return {
        "career_goal": career_goal,
        "learning_path": path_df,
        "total_courses": len(path_df),
        "total_duration": total_duration,
        "unresolved_prerequisites": unresolved_prerequisites,
        "skill_report": result["skill_report"]
    }


if __name__ == "__main__":

    user_skills = [
        "Python",
        "Pandas",
        "SQL"
    ]

    career_goal = "Data Scientist"

    result = generate_learning_path(
        user_skills=user_skills,
        career_goal=career_goal,
        top_n=5
    )

    print("\nPERSONALIZED LEARNING PATH")
    print("--------------------------")
    print("Career Goal:", result["career_goal"])

    if result["learning_path"].empty:
        print("No learning path could be generated.")

    else:
        print(
            result["learning_path"][
                [
                    "step",
                    "course_name",
                    "level",
                    "duration_hours",
                    "cumulative_duration"
                ]
            ].to_string(index=False)
        )

    print("\nTOTAL COURSES:", result["total_courses"])
    print("TOTAL DURATION:", result["total_duration"], "hours")

    print("\nUNRESOLVED PREREQUISITES")
    print("------------------------")
    print(result["unresolved_prerequisites"])