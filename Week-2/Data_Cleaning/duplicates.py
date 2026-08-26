import pandas as pd

# Create a dataset with duplicate records
data = {
    "Name": ["Ali", "Sara", "Ahmed", "Ali", "Sara", "Ayesha"],
    "Age": [21, 22, 20, 21, 22, 23],
    "Score": [85, 92, 78, 85, 92, 88]
}

df = pd.DataFrame(data)

print("Original Data:")
print(df)

# Check which rows are duplicated
print("\nDuplicated rows:")
print(df.duplicated())

# Count duplicate rows
print("\nNumber of duplicate rows:")
print(df.duplicated().sum())

# Display only the duplicated rows
print("\nDuplicate records:")
print(df[df.duplicated()])

# Remove duplicate rows
df_cleaned = df.drop_duplicates()

print("\nData after removing duplicates:")
print(df_cleaned)

# Compare number of rows before and after
print("\nOriginal number of rows:", len(df))
print("Cleaned number of rows:", len(df_cleaned))