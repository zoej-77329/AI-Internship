import pandas as pd

# Create a dataset with missing values
data = {
    "Name": ["Ali", "Sara", "Ahmed", None, "Usman"],
    "Age": [21, 22, None, 23, 20],
    "Score": [85, None, 78, 88, 95]
}

df = pd.DataFrame(data)

print("Original Data:")
print(df)

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

# isna() does the same thing as isnull()
print("\nMissing values using isna():")
print(df.isna().sum())

# Remove rows containing missing values
print("\nData after dropna():")
print(df.dropna())

# Fill missing values with a fixed value
df_filled = df.copy()

df_filled["Name"] = df_filled["Name"].fillna("Unknown")

# Fill Age with the mean age
df_filled["Age"] = df_filled["Age"].fillna(df_filled["Age"].mean())

# Fill Score with the mean score
df_filled["Score"] = df_filled["Score"].fillna(df_filled["Score"].mean())

print("\nData after filling missing values:")
print(df_filled)