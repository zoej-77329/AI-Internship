
import pandas as pd

# User profile
user = {
    "name": "Alex",
    "skills": ["Python", "Pandas", "NumPy"],
    "career_goal": "AI Engineer"
}

# Load career skills
df = pd.read_csv("Week-4/Recommendation-logic/dataset/career_skills.csv")

# Find required skills for user's career goal
career = df[df["career_goal"] == user["career_goal"]]

if not career.empty:

    required_skills = career.iloc[0]["required_skills"].split("|")

    current_skills = set(user["skills"])
    required_skills = set(required_skills)

    # Identify existing and missing skills
    existing_skills = current_skills.intersection(required_skills)

    missing_skills = required_skills.difference(current_skills)

    print("User:", user["name"])
    print("Career Goal:", user["career_goal"])

    print("\nExisting Required Skills:")
    print(sorted(existing_skills))

    print("\nMissing Skills:")
    print(sorted(missing_skills))

    print("\nTotal Missing Skills:", len(missing_skills))

else:
    print("Career goal not found!")
