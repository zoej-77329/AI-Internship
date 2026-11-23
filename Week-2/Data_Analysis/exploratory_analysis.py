import pandas as pd

# Load dataset
df = pd.read_csv("Week-2\Data_Analysis\dataset.csv")

# --------------------------------------------------
# 1. First look at the data
# --------------------------------------------------

print("First five rows:")
print(df.head())

print("\nLast five rows:")
print(df.tail())

# --------------------------------------------------
# 2. Dataset dimensions
# --------------------------------------------------

print("\nShape:")
print(df.shape)

# --------------------------------------------------
# 3. Column names
# --------------------------------------------------

print("\nColumns:")
print(df.columns)

# --------------------------------------------------
# 4. Data types
# --------------------------------------------------

print("\nData types:")
print(df.dtypes)

# --------------------------------------------------
# 5. Missing values
# --------------------------------------------------

print("\nMissing values:")
print(df.isnull().sum())

# --------------------------------------------------
# 6. Summary statistics
# --------------------------------------------------

print("\nSummary statistics:")
print(df.describe())

# --------------------------------------------------
# 7. Unique values
# --------------------------------------------------

print("\nUnique cities:")
print(df["City"].unique())

print("\nUnique categories:")
print(df["Category"].unique())

# --------------------------------------------------
# 8. Count values
# --------------------------------------------------

print("\nStudents by category:")
print(df["Category"].value_counts())

print("\nStudents by city:")
print(df["City"].value_counts())

print("\nStudents by gender:")
print(df["Gender"].value_counts())

# --------------------------------------------------
# 9. Average score
# --------------------------------------------------

print("\nAverage score:")
print(df["Score"].mean())

# --------------------------------------------------
# 10. Average score by category
# --------------------------------------------------

print("\nAverage score by category:")
print(df.groupby("Category")["Score"].mean())

# --------------------------------------------------
# 11. Average score by city
# --------------------------------------------------

print("\nAverage score by city:")
print(df.groupby("City")["Score"].mean())

# --------------------------------------------------
# 12. Highest score
# --------------------------------------------------

print("\nHighest score:")
print(df["Score"].max())

# --------------------------------------------------
# 13. Lowest score
# --------------------------------------------------

print("\nLowest score:")
print(df["Score"].min())

# --------------------------------------------------
# 14. Students scoring above 90
# --------------------------------------------------

print("\nStudents scoring above 90:")
print(df[df["Score"] > 90])


print("\nDataset information:")
df.info()
