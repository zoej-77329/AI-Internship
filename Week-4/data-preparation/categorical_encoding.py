
import pandas as pd
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("Week-4/data-preparation/dataset/users.csv")

# 1. Label Encoding
encoder = LabelEncoder()

df["experience_encoded"] = encoder.fit_transform(
    df["experience_level"]
)

print("Label Encoded Dataset:")
print(df[["experience_level", "experience_encoded"]])

# 2. One-Hot Encoding
courses = pd.read_csv("Week-4/data-preparation/dataset/courses.csv")

encoded_courses = pd.get_dummies(
    courses,
    columns=["category"],
    dtype=int
)

print("\nOne-Hot Encoded Dataset:")
print(encoded_courses.head())

# Save encoded dataset
encoded_courses.to_csv(
    "Week-4/data-preparation/dataset/courses_encoded.csv",
    index=False
)

print("\nEncoded dataset saved successfully!")
