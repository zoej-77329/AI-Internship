
courses = [
    {
        "name": "Statistics Fundamentals",
        "similarity": 75,
        "coverage": 50,
        "level_score": 100
    },
    {
        "name": "Machine Learning",
        "similarity": 90,
        "coverage": 75,
        "level_score": 80
    },
    {
        "name": "Deep Learning",
        "similarity": 95,
        "coverage": 50,
        "level_score": 40
    },
    {
        "name": "Data Analysis",
        "similarity": 80,
        "coverage": 25,
        "level_score": 100
    }
]

ranked_courses = []

for course in courses:

    final_score = (
        0.4 * course["similarity"] +
        0.4 * course["coverage"] +
        0.2 * course["level_score"]
    )

    ranked_courses.append({
        "name": course["name"],
        "score": round(final_score, 2)
    })

ranked_courses.sort(
    key=lambda x: x["score"],
    reverse=True
)

print("Final Course Rankings:\n")

for rank, course in enumerate(ranked_courses, start=1):

    print(
        rank,
        course["name"],
        "-",
        course["score"]
    )
