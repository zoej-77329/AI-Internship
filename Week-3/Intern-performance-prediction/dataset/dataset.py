
import numpy as np
import pandas as pd
from pathlib import Path

# Generate synthetic intern records
np.random.seed(42)

n = 500

data = {
    "intern_id": [f"INT-{i:03d}" for i in range(1, n + 1)],
    "task_completion_time": np.random.uniform(1, 12, n).round(2),
    "feedback_rating": np.random.uniform(1, 5, n).round(1),
    "attendance_rate": np.random.uniform(60, 100, n).round(2)
}

df = pd.DataFrame(data)

# Calculate performance scores
efficiency_score = np.clip(
    15 - (df["task_completion_time"] - 1) * 1.2,
    0,
    15
)

df["performance_score"] = (
    df["feedback_rating"] * 12
    + df["attendance_rate"] * 0.25
    + efficiency_score
    + np.random.normal(0, 3, n)
).clip(0, 100).round(2)

# Save dataset
output_path = Path(__file__).parent / "intern_performance.csv"

df.to_csv(output_path, index=False)

print("Dataset generated successfully!")
print("\nFirst five records:")
print(df.head())

print("\nDataset shape:", df.shape)
print("\nDataset information:")
print(df.describe())

print("\nSaved to:", output_path)
