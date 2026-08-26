import pandas as pd

data = {
    "Name": ["Ali", "Sara", "Ahmed"],
    "Age": ["21", "22", "20"],
    "Score": ["85", "92", "78"]
}

df = pd.DataFrame(data)

print("Original Data:")
print(df)

# Check data types
print("\nOriginal data types:")
print(df.dtypes)

# Convert Age from string to integer
df["Age"] = df["Age"].astype(int)

# Convert Score from string to integer
df["Score"] = df["Score"].astype(int)

print("\nData after conversion:")
print(df)

print("\nData types after conversion:")
print(df.dtypes)

# Perform numerical calculations
print("\nAverage Age:")
print(df["Age"].mean())

print("\nAverage Score:")
print(df["Score"].mean())

print("\nStudents with score above 80:")
print(df[df["Score"] > 80])