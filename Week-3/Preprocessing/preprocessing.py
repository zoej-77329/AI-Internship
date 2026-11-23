import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Create sample dataset
data = {
    "age": [20, 25, None, 35, 40],
    "salary": [30000, 40000, 50000, None, 70000],
    "department": ["IT", "HR", "IT", "Finance", "HR"]
}

df = pd.DataFrame(data)

print("Original Data:")
print(df)

# Handle missing numerical values
imputer = SimpleImputer(strategy="mean")

df[["age", "salary"]] = imputer.fit_transform(
    df[["age", "salary"]]
)

print("\nAfter Handling Missing Values:")
print(df)

# Scale numerical features
scaler = StandardScaler()

scaled_data = scaler.fit_transform(
    df[["age", "salary"]]
)

scaled_df = pd.DataFrame(
    scaled_data,
    columns=["age_scaled", "salary_scaled"]
)

print("\nScaled Numerical Data:")
print(scaled_df)

# Encode categorical data
encoder = OneHotEncoder(sparse_output=False)

encoded_data = encoder.fit_transform(
    df[["department"]]
)

encoded_df = pd.DataFrame(
    encoded_data,
    columns=encoder.get_feature_names_out(["department"])
)

print("\nEncoded Department:")
print(encoded_df)