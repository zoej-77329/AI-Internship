
courses = [
    {
        "name": "Python Fundamentals",
        "skills": ["Python", "Programming"],
        "level": "Beginner"
    },
    {
        "name": "Data Analysis",
        "skills": ["Python", "Pandas", "NumPy"],
        "level": "Beginner"
    },
    {
        "name": "Machine Learning",
        "skills": ["Python", "Statistics", "ML"],
        "level": "Intermediate"
    },
    {
        "name": "Deep Learning",
        "skills": ["Python", "Neural Networks", "ML"],
        "level": "Advanced"
    },
    {
        "name": "Web Development",
        "skills": ["HTML", "CSS", "JavaScript"],
        "level": "Beginner"
    }
]

user = {
    "name": "Alex",
    "skills": ["Python", "Programming"],
    "interests": ["Machine Learning", "AI"],
    "level": "Beginner"
}

print("User:", user["name"])
print("User Skills:", user["skills"])
print("\nCourse Recommendations:")

for course in courses:

    course_skills = set(course["skills"])
    user_skills = set(user["skills"])

    common_skills = course_skills.intersection(user_skills)

    if common_skills:
        match_percentage = (
            len(common_skills) / len(course_skills)
        ) * 100

        print("\nCourse:", course["name"])
        print("Matching Skills:", list(common_skills))
        print("Match Percentage:", round(match_percentage, 2), "%")
