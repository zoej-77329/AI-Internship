
import pandas as pd

# Load messy dataset
df = pd.read_csv("Week-4/data-preparation/dataset/courses_messy.csv")

print("Original Dataset:")
print(df)

# 1. Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# 2. Remove duplicate records
df = df.drop_duplicates()

# 3. Remove records with missing course names
df = df.dropna(subset=["course_name"])

# 4. Fill missing duration with median
df["duration_hours"] = df["duration_hours"].fillna(
    df["duration_hours"].median()
)

# 5. Remove negative durations
df = df[df["duration_hours"] > 0]

# 6. Standardize text columns
df["course_name"] = df["course_name"].str.strip()

df["level"] = df["level"].str.strip().str.title()

df["category"] = df["category"].str.strip().str.title()

# 7. Reset index
df = df.reset_index(drop=True)

print("\nCleaned Dataset:")
print(df)

# 8. Verify missing values and duplicates
print("\nRemaining Missing Values:")
print(df.isnull().sum())

print("\nRemaining Duplicates:")
print(df.duplicated().sum())

# 9. Save cleaned dataset
df.to_csv("Week-4/data-preparation/dataset/courses_cleaned.csv", index=False)

print("\nCleaned dataset saved successfully!")
