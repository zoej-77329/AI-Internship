
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


# 1. Display all course names
print("Available Courses:")

for course in courses:
    print(course["name"])


# 2. Display beginner-level courses
print("\nBeginner Courses:")

for course in courses:
    if course["level"] == "Beginner":
        print(course["name"])


# 3. Find courses that teach Python
print("\nCourses Teaching Python:")

for course in courses:
    if "Python" in course["skills"]:
        print(course["name"])


# 4. Count total courses
print("\nTotal Courses:", len(courses))


# 5. Display all unique skills
all_skills = set()

for course in courses:
    for skill in course["skills"]:
        all_skills.add(skill)

print("\nUnique Skills:")
print(sorted(all_skills))
