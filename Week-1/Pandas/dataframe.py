import pandas as pd


data = {
    "Name": ["Ali", "Sara", "Ahmed", "Ayesha"],
    "Age": [21, 22, 20, 23],
    "Score": [85, 92, 78, 95]
}

df = pd.DataFrame(data)

print(df)
print(df["Name"])
print(df["Score"])