import pandas as pd

data = {
    "Department": ["SE", "CS", "SE", "AI", "CS"],
    "Score": [85, 90, 78, 95, 88]
}

df = pd.DataFrame(data)

print("Average:", df["Score"].mean())
print("Highest:", df["Score"].max())
print("Lowest:", df["Score"].min())

print("\nAverage score by department:")
print(df.groupby("Department")["Score"].mean())