import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Create dataset
data = {
    "size": [1000, 1200, 1500, 1800, 2000, 2200, 2500, 2800],
    "price": [200000, 240000, 300000, 360000, 400000, 440000, 500000, 560000]
}

df = pd.DataFrame(data)

# Features and target
X = df[["size"]]
y = df["price"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create and train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Predictions:", y_pred)
print("Actual:", y_test.values)

print("MAE:", mae)
print("MSE:", mse)
print("R2 Score:", r2)