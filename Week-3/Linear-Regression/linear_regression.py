import numpy as np
from sklearn.linear_model import LinearRegression

# Training data
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

# Create model
model = LinearRegression()

# Train model
model.fit(X, y)

# Make prediction
prediction = model.predict([[6]])

print("Prediction:", prediction)

print("Slope:", model.coef_)
print("Intercept:", model.intercept_)