# Student Performance Prediction

## Objective

The objective of this project is to build a machine learning model that predicts whether a student is likely to pass based on academic and study-related features.

## Features Used

- Study hours
- Attendance
- Assignments completed
- Previous score

## Target

The target variable is:

- `1` = Passed
- `0` = Failed

## Machine Learning Algorithm

Logistic Regression was used because this is a binary classification problem.

## Workflow

1. Load the dataset
2. Check the dataset
3. Separate features and target
4. Split the data into training and testing sets
5. Scale numerical features
6. Train the Logistic Regression model
7. Make predictions
8. Evaluate the model
9. Predict the result for a new student

## Evaluation Metrics

The model was evaluated using:

- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix

## Important Note

This dataset is a small educational dataset created for learning purposes. The model should not be used for real-world student assessment or academic decisions.

## Technologies

- Python
- Pandas
- Scikit-learn