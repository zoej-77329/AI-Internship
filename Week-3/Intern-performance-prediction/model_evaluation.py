
import pandas as pd
from pathlib import Path
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

BASE_DIR = Path(__file__).parent
RESULTS_DIR = BASE_DIR / "results"

# Load predictions
rf = pd.read_csv(
    RESULTS_DIR / "random_forest_predictions.csv"
)

xgb = pd.read_csv(
    RESULTS_DIR / "xgboost_predictions.csv"
)

# Verify actual test records match
assert (rf["Actual Score"] == xgb["Actual Score"]).all()

# Calculate metrics
models = {
    "Random Forest": rf["Predicted Score"],
    "XGBoost": xgb["Predicted Score"]
}

actual = rf["Actual Score"]

results = []

for name, predicted in models.items():

    mse = mean_squared_error(actual, predicted)

    results.append({
        "Model": name,
        "MAE": mean_absolute_error(actual, predicted),
        "MSE": mse,
        "RMSE": mse ** 0.5,
        "R2 Score": r2_score(actual, predicted)
    })

comparison = pd.DataFrame(results)

print("\nModel Performance Comparison")
print("----------------------------")
print(comparison.round(4).to_string(index=False))

# Identify best model based on R2
best_model = comparison.loc[
    comparison["R2 Score"].idxmax(), "Model"
]

print("\nBest Performing Model:", best_model)

# Save comparison
comparison.to_csv(
    RESULTS_DIR / "model_comparison.csv",
    index=False
)

print("\nComparison saved successfully!")
