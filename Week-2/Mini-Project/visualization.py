import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Week-2\Data_Analysis\dataset.csv")

# Remove duplicates and missing values
df = df.drop_duplicates()
df = df.dropna()


# ==========================================
# 1. BAR CHART
# ==========================================

category_scores = df.groupby("Category")["Score"].mean()

plt.figure()
plt.bar(category_scores.index, category_scores.values)

plt.title("Average Score by Category")
plt.xlabel("Category")
plt.ylabel("Average Score")

plt.savefig("Week-2/visualizations/category_average_scores.png")

plt.show()


# ==========================================
# 2. SCATTER PLOT
# ==========================================

plt.figure()
plt.scatter(df["Age"], df["Score"])

plt.title("Age vs Score")
plt.xlabel("Age")
plt.ylabel("Score")

plt.savefig("Week-2/visualizations/age_vs_score.png")

plt.show()


# ==========================================
# 3. HISTOGRAM
# ==========================================

plt.figure()
plt.hist(df["Score"], bins=5)

plt.title("Score Distribution")
plt.xlabel("Score")
plt.ylabel("Frequency")

plt.savefig("Week-2/visualizations/score_distribution.png")

plt.show()