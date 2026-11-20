from data_loader import load_courses


def generate_learning_path(user_skills, required_skills):

    courses = load_courses()

    current_skills = set(user_skills)
    required_skills = set(required_skills)

    remaining_skills = required_skills - current_skills

    learning_path = []
    used_courses = set()

    while remaining_skills:

        best_course = None
        best_coverage = set()

        for _, course in courses.iterrows():

            course_id = course["course_id"]

            if course_id in used_courses:
                continue

            prerequisites = course.get("prerequisites", "")

            if isinstance(prerequisites, str) and prerequisites.strip():
                prerequisite_skills = {
                    skill.strip()
                    for skill in prerequisites.split("|")
                    if skill.strip()
                }
            else:
                prerequisite_skills = set()

            # Check prerequisites
            if not prerequisite_skills.issubset(current_skills):
                continue

            course_skills = set(course["skills"])

            covered_skills = course_skills.intersection(
                remaining_skills
            )

            if len(covered_skills) > len(best_coverage):
                best_course = course
                best_coverage = covered_skills

        if best_course is None or not best_coverage:
            break

        learning_path.append(best_course["course_name"])

        used_courses.add(best_course["course_id"])

        # Assume the user completes this course successfully
        current_skills.update(best_course["skills"])

        remaining_skills = required_skills - current_skills

    return learning_path, remaining_skills