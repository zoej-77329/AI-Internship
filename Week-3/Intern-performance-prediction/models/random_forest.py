
import pandas as pd
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "intern_performance.csv"
RESULTS_DIR = BASE_DIR / "results"

# Load dataset
df = pd.read_csv(DATA_PATH)

# Select features and target
X = df[
    [
        "task_completion_time",
        "feedback_rating",
        "attendance_rate"
    ]
]

y = df["performance_score"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create Random Forest model
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=5,
    random_state=42
)

# Train model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate model
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
r2 = r2_score(y_test, y_pred)

print("Random Forest Regression Results")
print("--------------------------------")

print("MAE:", round(mae, 2))
print("MSE:", round(mse, 2))
print("RMSE:", round(rmse, 2))
print("R2 Score:", round(r2, 4))

# Feature importance
importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

print("\nFeature Importance:")
print(importance.sort_values(
    by="Importance",
    ascending=False
))

# Save trained model
joblib.dump(
    model,
    RESULTS_DIR / "random_forest_model.pkl"
)

# Save predictions
predictions = pd.DataFrame({
    "Actual Score": y_test.values,
    "Predicted Score": y_pred
})

predictions.to_csv(
    RESULTS_DIR / "random_forest_predictions.csv",
    index=False
)

print("\nRandom Forest model trained successfully!")
print("Model and predictions saved.")
