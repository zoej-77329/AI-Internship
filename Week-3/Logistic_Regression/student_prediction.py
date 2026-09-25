import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Create dataset
data = {
    "study_hours": [1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7],
    "attendance": [55, 60, 65, 70, 72, 75, 78, 82, 85, 88, 90, 95],
    "passed": [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
}

df = pd.DataFrame(data)

# Features and target
X = df[["study_hours", "attendance"]]
y = df["passed"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# Create model
model = LogisticRegression()

# Train model
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Predict a new student
new_student = [[5, 85]]

prediction = model.predict(new_student)

if prediction[0] == 1:
    print("\nPrediction: Student is likely to pass.")
else:
    print("\nPrediction: Student is likely to fail.")