
courses = [
    {
        "name": "Data Analysis",
        "skills": ["Python", "Pandas", "NumPy"],
        "category": "Data Science"
    },
    {
        "name": "Machine Learning",
        "skills": ["Python", "Statistics", "ML"],
        "category": "Artificial Intelligence"
    },
    {
        "name": "Deep Learning",
        "skills": ["Python", "Neural Networks", "ML"],
        "category": "Artificial Intelligence"
    },
    {
        "name": "Web Development",
        "skills": ["HTML", "CSS", "JavaScript"],
        "category": "Web Development"
    },
    {
        "name": "Data Visualization",
        "skills": ["Python", "Matplotlib", "Seaborn"],
        "category": "Data Science"
    },
    {
    "name": "Computer Vision",
    "skills": ["Python", "OpenCV", "Deep Learning"],
    "category": "Artificial Intelligence"
    }
]

user = {
    "skills": ["Python", "Pandas"],
    "interests": ["Artificial Intelligence", "Data Science"],
    "career_goal": "AI Engineer"
}

recommendations = []

for course in courses:

    if course["category"] in user["interests"]:

        recommendations.append(course)

print("Recommended Courses:\n")

for course in recommendations:
    print(course["name"], "-", course["category"])
