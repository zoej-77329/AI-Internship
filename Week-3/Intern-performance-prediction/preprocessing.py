
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

# Load dataset
BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "dataset" / "intern_performance.csv"
RESULTS_DIR = BASE_DIR / "results"

RESULTS_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_PATH)

print("Original Dataset:")
print(df.head())

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Remove duplicate records
df = df.drop_duplicates()

# Separate features and target
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

# Scale numerical features
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save processed datasets
pd.DataFrame(
    X_train_scaled,
    columns=X.columns
).to_csv(RESULTS_DIR / "X_train.csv", index=False)

pd.DataFrame(
    X_test_scaled,
    columns=X.columns
).to_csv(RESULTS_DIR / "X_test.csv", index=False)

y_train.to_csv(RESULTS_DIR / "y_train.csv", index=False)
y_test.to_csv(RESULTS_DIR / "y_test.csv", index=False)

joblib.dump(scaler, RESULTS_DIR / "scaler.pkl")

print("\nPreprocessing Completed!")
print("Training records:", len(X_train))
print("Testing records:", len(X_test))
print("Processed datasets saved successfully.")
