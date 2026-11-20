
courses = [
    {
        "name": "Statistics for Data Science",
        "skills": ["Statistics", "Probability"]
    },
    {
        "name": "Machine Learning",
        "skills": ["Python", "Statistics", "Machine Learning"]
    },
    {
        "name": "Deep Learning",
        "skills": ["Python", "Neural Networks", "Machine Learning"]
    },
    {
        "name": "Computer Vision",
        "skills": ["Python", "OpenCV", "Deep Learning"]
    },
    {
        "name": "Web Development",
        "skills": ["HTML", "CSS", "JavaScript"]
    }
]

missing_skills = {
    "Statistics",
    "Machine Learning",
    "Deep Learning",
    "Neural Networks"
}

ranked_courses = []

for course in courses:

    course_skills = set(course["skills"])

    covered_skills = course_skills.intersection(
        missing_skills
    )

    coverage_score = (
        len(covered_skills) / len(missing_skills)
    ) * 100

    ranked_courses.append({
        "name": course["name"],
        "covered_skills": list(covered_skills),
        "score": round(coverage_score, 2)
    })

# Sort courses by score
ranked_courses.sort(
    key=lambda x: x["score"],
    reverse=True
)

print("Ranked Courses:\n")

for course in ranked_courses:

    print("Course:", course["name"])
    print("Covered Skills:", course["covered_skills"])
    print("Coverage Score:", course["score"], "%")
    print()
