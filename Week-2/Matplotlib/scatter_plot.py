import matplotlib.pyplot as plt

study_hours = [1, 2, 3, 4, 5, 6]
scores = [50, 55, 62, 70, 78, 88]

plt.scatter(study_hours, scores)

plt.title("Study Hours vs Score")
plt.xlabel("Study Hours")
plt.ylabel("Score")

plt.savefig("Week-2/visualizations/scatter_plot.png")

plt.show()