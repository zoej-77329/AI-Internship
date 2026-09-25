import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


# -----------------------------------
# 1. Load Dataset
# -----------------------------------

df = pd.read_csv("Week-3\\Mini_Project\\dataset.csv")

print("Dataset:")
print(df)

print("\nDataset Information:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())


# -----------------------------------
# 2. Separate Features and Target
# -----------------------------------

X = df[
    [
        "study_hours",
        "attendance",
        "assignments_completed",
        "previous_score"
    ]
]

y = df["passed"]


# -----------------------------------
# 3. Split Dataset
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# -----------------------------------
# 4. Feature Scaling
# -----------------------------------

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# -----------------------------------
# 5. Create Model
# -----------------------------------

model = LogisticRegression(
    random_state=42
)


# -----------------------------------
# 6. Train Model
# -----------------------------------

model.fit(
    X_train_scaled,
    y_train
)


# -----------------------------------
# 7. Make Predictions
# -----------------------------------

y_pred = model.predict(
    X_test_scaled
)


# -----------------------------------
# 8. Evaluate Model
# -----------------------------------

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)


print("\n--- Model Evaluation ---")

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)


print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# -----------------------------------
# 9. Predict New Student
# -----------------------------------

new_student = pd.DataFrame(
    [
        {
            "study_hours": 6,
            "attendance": 88,
            "assignments_completed": 8,
            "previous_score": 75
        }
    ]
)

new_student_scaled = scaler.transform(
    new_student
)

prediction = model.predict(
    new_student_scaled
)

probability = model.predict_proba(
    new_student_scaled
)


print("\n--- New Student Prediction ---")

if prediction[0] == 1:
    print("Prediction: Likely to Pass")
else:
    print("Prediction: Likely to Fail")

print(
    "Probability of passing:",
    probability[0][1]
)
