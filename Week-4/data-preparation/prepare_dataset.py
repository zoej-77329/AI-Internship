
import pandas as pd

# Load cleaned course data
courses = pd.read_csv("Week-4/data-preparation/dataset/courses_cleaned.csv")

# Load user data
users = pd.read_csv("Week-4/data-preparation/dataset/users.csv")

# Convert skills into lists
courses["skills"] = courses["skills"].str.lower().str.split("|")
users["skills"] = users["skills"].str.lower().str.split("|")

# Convert interests into lists
users["interests"] = users["interests"].str.lower().str.split("|")

# Display prepared data
print("Prepared Courses:")
print(courses[["course_name", "skills", "level"]])

print("\nPrepared Users:")
print(users[["name", "skills", "interests"]])

# Validate datasets
print("\nDataset Validation")

print("Course records:", len(courses))
print("User records:", len(users))

print("Missing course names:", courses["course_name"].isnull().sum())
print("Missing user names:", users["name"].isnull().sum())

print("\nDataset preparation completed!")
