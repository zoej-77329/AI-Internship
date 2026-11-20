
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

# Sample course data
courses = pd.DataFrame({
    "course": [
        "Python Fundamentals",
        "Data Analysis",
        "Machine Learning",
        "Web Development"
    ],
    "skills": [
        ["Python", "Programming"],
        ["Python", "Pandas", "NumPy"],
        ["Python", "Statistics", "ML"],
        ["HTML", "CSS", "JavaScript"]
    ]
})

# Convert skills into binary features
encoder = MultiLabelBinarizer()

skill_vectors = encoder.fit_transform(courses["skills"])

# Create encoded DataFrame
encoded_df = pd.DataFrame(
    skill_vectors,
    columns=encoder.classes_
)

print("Skill Vocabulary:")
print(encoder.classes_)

print("\nEncoded Skill Vectors:")
print(encoded_df)

print("\nCourse Names:")
print(courses["course"])
