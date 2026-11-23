
courses = [
    {
        "name": "Python Fundamentals",
        "skills": ["Python", "Programming"],
        "prerequisites": [],
        "level": "Beginner"
    },
    {
        "name": "Statistics Fundamentals",
        "skills": ["Statistics", "Probability"],
        "prerequisites": [],
        "level": "Beginner"
    },
    {
        "name": "Data Analysis",
        "skills": ["Pandas", "NumPy"],
        "prerequisites": ["Python"],
        "level": "Beginner"
    },
    {
        "name": "Machine Learning",
        "skills": ["Machine Learning", "ML"],
        "prerequisites": ["Python", "Statistics"],
        "level": "Intermediate"
    },
    {
        "name": "Deep Learning",
        "skills": ["Neural Networks", "Deep Learning"],
        "prerequisites": ["Python", "Machine Learning"],
        "level": "Advanced"
    }
]

user = {
    "name": "Alex",
    "skills": ["Python"],
    "career_goal": "AI Engineer"
}

required_skills = {
    "Python",
    "Statistics",
    "Machine Learning",
    "Neural Networks",
    "Deep Learning"
}

current_skills = set(user["skills"])

missing_skills = required_skills - current_skills

learning_path = []
completed_courses = set()

while missing_skills:

    eligible_courses = []

    for course in courses:

        if course["name"] in completed_courses:
            continue

        prerequisites = set(course["prerequisites"])

        if prerequisites.issubset(current_skills):

            coverage = set(course["skills"]) & missing_skills

            if coverage:
                eligible_courses.append({
                    "course": course,
                    "coverage": coverage
                })

    if not eligible_courses:
        break

    # Select course covering the most missing skills
    selected = max(
        eligible_courses,
        key=lambda x: len(x["coverage"])
    )

    course = selected["course"]

    learning_path.append(course["name"])

    completed_courses.add(course["name"])

    current_skills.update(course["skills"])

    missing_skills = required_skills - current_skills

print("User:", user["name"])
print("Career Goal:", user["career_goal"])

print("\nRecommended Learning Path:")

for index, course in enumerate(learning_path, start=1):
    print(f"{index}. {course}")

print("\nRemaining Skill Gaps:")
print(sorted(missing_skills))

if not missing_skills:
    print("\nAll required skills are covered!")
