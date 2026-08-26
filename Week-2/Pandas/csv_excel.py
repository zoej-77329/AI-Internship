import pandas as pd

df = pd.read_csv("Week-1/Pandas/students.csv")

print(df)

print(df.head())

print(df.tail())

print(df.shape)

print(df.columns)

df.to_csv("Week-2/Pandas/output.csv", index=False)

df = pd.read_excel("Week-1/Pandas/students.xlsx")

df.to_excel("Week-2/Pandas/output.xlsx", index=False)