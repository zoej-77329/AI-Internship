import pandas as pd

# Create a dataset with common data-quality problems
data = {
    "Name": ["Ali", "Sara", "Ahmed", "Ayesha", "Usman"],
    "Age": [21, 22, 20, None, 20],
    "Score": [85, 92, 78, 105, None],
    "City": ["Lahore ", "Karachi", "Lahore", "Islamabad", "Karachi "],
    "Email": [
        "ali@gmail.com",
        "sara@gmail.com",
        "ahmed@gmail.com",
        "ayesha@gmail.com",
        "usman@gmail.com"
    ],
    "Unnecessary": [1, 2, 3, 4, 5]
}

df = pd.DataFrame(data)

print("Original Data:")
print(df)

# --------------------------------------------------
# 1. Remove unnecessary columns
# --------------------------------------------------

df.drop(columns=["Unnecessary"], inplace=True)

print("\nAfter removing unnecessary column:")
print(df)

# --------------------------------------------------
# 2. Rename columns
# --------------------------------------------------

df.rename(columns={"Score": "Exam_Score"}, inplace=True)

print("\nAfter renaming Score:")
print(df)

# --------------------------------------------------
# 3. Remove extra spaces from City
# --------------------------------------------------

df["City"] = df["City"].str.strip()

print("\nAfter removing extra spaces:")
print(df)

# --------------------------------------------------
# 4. Replace inconsistent values
# --------------------------------------------------

df["City"] = df["City"].replace({
    "Lahore": "Lahore",
    "Karachi": "Karachi",
    "Islamabad": "Islamabad"
})

print("\nAfter replacing city values:")
print(df)

# --------------------------------------------------
# 5. Handle missing values
# --------------------------------------------------

df["Age"] = df["Age"].fillna(df["Age"].mean())

df["Exam_Score"] = df["Exam_Score"].fillna(
    df["Exam_Score"].mean()
)

print("\nAfter filling missing values:")
print(df)

# --------------------------------------------------
# 6. Filter invalid rows
# --------------------------------------------------

df = df[df["Exam_Score"] <= 100]

print("\nAfter removing invalid scores:")
print(df)

# --------------------------------------------------
# Final cleaned dataset
# --------------------------------------------------

print("\nFinal Cleaned Data:")
print(df)