import pandas as pd

# Load dataset
df = pd.read_csv("Week-2\Data_Analysis\dataset.csv")

print("========== DATASET OVERVIEW ==========")

print("\nFirst five rows:")
print(df.head())

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())


# ==========================================
# DATA CLEANING
# ==========================================

# Remove duplicate rows
df = df.drop_duplicates()

# Remove rows with missing values
df = df.dropna()

print("\n========== AFTER CLEANING ==========")

print("\nShape:")
print(df.shape)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

# ==========================================
# ANALYSIS
# ==========================================

print("\n========== ANALYSIS ==========")

print("\nAverage Score:")
print(df["Score"].mean())

print("\nHighest Score:")
print(df["Score"].max())

print("\nLowest Score:")
print(df["Score"].min())

print("\nAverage Score by Category:")
print(df.groupby("Category")["Score"].mean())

print("\nAverage Score by City:")
print(df.groupby("City")["Score"].mean())

print("\nNumber of Students by Category:")
print(df["Category"].value_counts())

print("\nNumber of Students by City:")
print(df["City"].value_counts())

print("\nStudents scoring above 90:")
print(df[df["Score"] > 90])

print("\nStudent with highest score:")
print(df.loc[df["Score"].idxmax()])