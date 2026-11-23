import pandas as pd

# Student information
students = pd.DataFrame({
    "Student_ID": [1, 2, 3, 4],
    "Name": ["Ali", "Sara", "Ahmed", "Ayesha"]
})

# Student scores
scores = pd.DataFrame({
    "Student_ID": [1, 2, 3, 5],
    "Score": [85, 92, 78, 90]
})

print("Students:")
print(students)

print("\nScores:")
print(scores)

# --------------------------------------------------
# INNER MERGE
# --------------------------------------------------

inner_result = pd.merge(
    students,
    scores,
    on="Student_ID",
    how="inner"
)

print("\nInner Merge:")
print(inner_result)

# --------------------------------------------------
# LEFT MERGE
# --------------------------------------------------

left_result = pd.merge(
    students,
    scores,
    on="Student_ID",
    how="left"
)

print("\nLeft Merge:")
print(left_result)

# --------------------------------------------------
# RIGHT MERGE
# --------------------------------------------------

right_result = pd.merge(
    students,
    scores,
    on="Student_ID",
    how="right"
)

print("\nRight Merge:")
print(right_result)

# --------------------------------------------------
# OUTER MERGE
# --------------------------------------------------

outer_result = pd.merge(
    students,
    scores,
    on="Student_ID",
    how="outer"
)

print("\nOuter Merge:")
print(outer_result)