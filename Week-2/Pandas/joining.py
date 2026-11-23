import pandas as pd

# First DataFrame
df1 = pd.DataFrame({
    "Name": ["Ali", "Sara", "Ahmed"],
    "City": ["Lahore", "Multan", "Islamabad"]
}, index=[1, 2, 3])

# Second DataFrame
df2 = pd.DataFrame({
    "Score": [85, 92, 78],
    "Grade": ["A", "A", "B"]
}, index=[1, 2, 4])

print("DataFrame 1:")
print(df1)

print("\nDataFrame 2:")
print(df2)

# Join the two DataFrames
result = df1.join(df2)

print("\nJoined DataFrame:")
print(result)