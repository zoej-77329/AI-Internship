
courses = [
    {
        "name": "Python Fundamentals",
        "prerequisites": [],
        "skills": ["Python", "Programming"]
    },
    {
        "name": "Statistics Fundamentals",
        "prerequisites": [],
        "skills": ["Statistics", "Probability"]
    },
    {
        "name": "Data Analysis",
        "prerequisites": ["Python"],
        "skills": ["Pandas", "NumPy"]
    },
    {
        "name": "Machine Learning",
        "prerequisites": ["Python", "Statistics"],
        "skills": ["Machine Learning", "ML"]
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

user_skills = {"Python"}

print("Available Courses:\n")

for course in courses:

    required = set(course["prerequisites"])

    if required.issubset(user_skills):

        print("Eligible:", course["name"])

    else:

        missing = required.difference(user_skills)

        print("Not Eligible:", course["name"])
        print("Missing Prerequisites:", sorted(missing))
        print()
