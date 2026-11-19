
# Intern Performance Prediction Model

## Overview

The Intern Performance Prediction Model is a Machine Learning project that predicts intern performance based on task completion time, feedback ratings, and attendance records.

The project uses Random Forest Regression and XGBoost Regression to predict performance scores and compares both models to identify the better-performing model.

An interactive dashboard built with Streamlit and Plotly displays performance analysis, model evaluation results, and individual intern predictions.

## Objectives

- Predict intern performance using Machine Learning.
- Analyze task completion time, feedback ratings, and attendance.
- Implement Random Forest and XGBoost regression models.
- Compare model performance using evaluation metrics.
- Visualize results through an interactive dashboard.

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- Streamlit
- Plotly
- Matplotlib
- Joblib
- Git and GitHub

## Project Structure

```text
Intern-Performance-Prediction/
│
├── dataset/
│   ├── generate_dataset.py
│   └── intern_performance.csv
│
├── models/
│   ├── random_forest.py
│   └── xgboost_model.py
│
├── results/
│
├── preprocessing.py
├── model_evaluation.py
├── dashboard.py
├── requirements.txt
└── README.md
```

## Dataset

The project uses a synthetic dataset containing 500 intern records.

Features:
- Intern ID
- Task completion time
- Feedback rating
- Attendance rate

Target:
- Performance score (0-100)

The dataset is synthetically generated for educational purposes because actual company intern performance records were not available.

## Machine Learning Models

### 1. Random Forest Regression

Uses multiple decision trees to predict intern performance scores.

### 2. XGBoost Regression

Uses gradient boosting to improve prediction performance by combining multiple decision trees.

## Model Evaluation

Both models are evaluated using:

- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R² Score

### Results

| Metric | Random Forest | XGBoost |
|---|---:|---:|
| MAE | 3.2705 | 3.1783 |
| MSE | 17.4381 | 15.6610 |
| RMSE | 4.1759 | 3.9574 |
| R² Score | 0.9165 | 0.9250 |

XGBoost achieved better results across all four evaluation metrics on the test dataset.

## Dashboard Features

- Intern performance overview
- Performance category distribution
- Feature importance visualization
- Attendance and performance analysis
- Feedback rating analysis
- Random Forest and XGBoost comparison
- Actual vs predicted score visualization
- Individual intern performance prediction
- Downloadable prediction report

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
```

Navigate to the project folder:

```bash
cd Week-3/Intern-Performance-Prediction
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate the dataset:

```bash
python dataset/generate_dataset.py
```

Run preprocessing:

```bash
python preprocessing.py
```

Train Random Forest:

```bash
python models/random_forest.py
```

Train XGBoost:

```bash
python models/xgboost_model.py
```

Compare models:

```bash
python model_evaluation.py
```

Launch dashboard:

```bash
python -m streamlit run dashboard.py
```

## Limitations

- The dataset contains simulated records rather than actual company data.
- Model performance reflects the synthetic data generation formula.
- Predictions should not be used for real employee evaluation or hiring decisions.

## Conclusion

This project demonstrates the application of Machine Learning regression algorithms for performance prediction. Random Forest and XGBoost were implemented and evaluated, with XGBoost achieving a slightly better performance on the synthetic test dataset.
