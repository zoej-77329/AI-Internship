
courses = [
    {
        "name": "Python Fundamentals",
        "prerequisites": [],
        "skills": ["Python"]
    },
    {
        "name": "Statistics Fundamentals",
        "prerequisites": [],
        "skills": ["Statistics"]
    },
    {
        "name": "Data Analysis",
        "prerequisites": ["Python"],
        "skills": ["Pandas", "NumPy"]
    },
    {
        "name": "Machine Learning",
        "prerequisites": ["Python", "Statistics"],
        "skills": ["Machine Learning"]
    },
    {
        "name": "Deep Learning",
        "prerequisites": ["Python", "Machine Learning"],
        "skills": ["Neural Networks", "Deep Learning"]
    },
    {
        "name": "Computer Vision",
        "prerequisites": ["Python", "Deep Learning"],
        "skills": ["OpenCV", "Image Processing"]
    }
]

user_skills = set()

completed_courses = set()

learning_path = []

while True:

    available_courses = []

    for course in courses:

        if course["name"] in completed_courses:
            continue

        required = set(course["prerequisites"])

        if required.issubset(user_skills):

            available_courses.append(course)

    if not available_courses:
        break

    # Select the first eligible course
    selected_course = available_courses[0]

    learning_path.append(selected_course["name"])

    completed_courses.add(selected_course["name"])

    # Update user skills after completing course
    user_skills.update(selected_course["skills"])

print("Recommended Learning Path:\n")

for index, course in enumerate(learning_path, start=1):

    print(f"{index}. {course}")

print("\nSkills After Learning:")
print(sorted(user_skills))
