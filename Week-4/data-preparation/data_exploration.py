
import pandas as pd

# Load datasets
courses = pd.read_csv("Week-4/data-preparation/dataset/courses.csv")
users = pd.read_csv("Week-4/data-preparation/dataset/users.csv")

# Display datasets
print("COURSES DATASET")
print(courses)

print("\nUSERS DATASET")
print(users)


# 1. Display first five records
print("\nFirst 5 Courses:")
print(courses.head())

# 2. Display last five records
print("\nLast 5 Courses:")
print(courses.tail())

# 3. Check dataset dimensions
print("\nDataset Shape:")
print(courses.shape)

# 4. Check column names
print("\nColumn Names:")
print(courses.columns)

# 5. Check data types
print("\nData Types:")
print(courses.dtypes)

# 6. Dataset information
print("\nDataset Information:")
courses.info()

# 7. Statistical summary
print("\nStatistical Summary:")
print(courses.describe())

# 8. Check missing values
print("\nMissing Values:")
print(courses.isnull().sum())

# 9. Count unique values
print("\nUnique Course Levels:")
print(courses["level"].unique())

# 10. Count courses by category
print("\nCourses by Category:")
print(courses["category"].value_counts())
