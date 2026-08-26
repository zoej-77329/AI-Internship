import matplotlib.pyplot as plt

scores = [
    45, 50, 52, 55, 60, 61, 65,
    68, 70, 72, 75, 80, 85, 90
]

plt.hist(scores, bins=5)

plt.title("Score Distribution")
plt.xlabel("Score")
plt.ylabel("Frequency")

plt.savefig("Week-2/visualizations/histogram.png")

plt.show()