
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

courses = [
    {
        "name": "Data Analysis",
        "description": "Python Pandas NumPy data analysis"
    },
    {
        "name": "Machine Learning",
        "description": "Python Statistics Machine Learning ML"
    },
    {
        "name": "Deep Learning",
        "description": "Python Neural Networks Deep Learning ML"
    },
    {
        "name": "Web Development",
        "description": "HTML CSS JavaScript web development"
    },
    {
        "name": "Computer Vision",
        "description": "Python OpenCV Deep Learning image processing"
    }
]

user = {
    "skills": "Python Pandas",
    "interests": "Artificial Intelligence Machine Learning",
    "goal": "AI Engineer"
}

# Combine user information
user_profile = (
    user["skills"] + " " +
    user["interests"] + " " +
    user["goal"]
)

# Extract course descriptions
course_descriptions = [
    course["description"] for course in courses
]

# Combine user profile and course descriptions
documents = [user_profile] + course_descriptions

# Convert text into TF-IDF vectors
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(documents)

# Compare user profile with courses
scores = cosine_similarity(
    vectors[0:1],
    vectors[1:]
)[0]

# Store recommendation scores
recommendations = []

for course, score in zip(courses, scores):
    recommendations.append({
        "course": course["name"],
        "similarity": round(float(score), 3)
    })

# Sort by similarity
recommendations.sort(
    key=lambda x: x["similarity"],
    reverse=True
)

# Display recommendations
print("Recommended Courses:\n")

for item in recommendations:
    print(
        item["course"],
        "->",
        item["similarity"]
    )
