
import pandas as pd

df = pd.read_csv("Week-4/data-preparation/dataset/users.csv")

# Convert text into lowercase and remove spaces
df["name"] = df["name"].str.strip().str.lower()

# Convert skill strings into lists
df["skills"] = df["skills"].str.lower().str.split("|")

# Convert interests into lists
df["interests"] = df["interests"].str.lower().str.split("|")

# Standardize experience level and career goal
df["experience_level"] = (
    df["experience_level"].str.strip().str.lower()
)

df["career_goal"] = (
    df["career_goal"].str.strip().str.lower()
)

print("Preprocessed User Dataset:")
print(df)

print("\nSkills of First User:")
print(df.loc[0, "skills"])

print("\nInterests of First User:")
print(df.loc[0, "interests"])
