import matplotlib.pyplot as plt

# Data
categories = ["A", "B", "C", "D"]
values = [40, 65, 30, 80]

# Create bar chart
plt.bar(categories, values)

# Add title and labels
plt.title("Category Comparison")
plt.xlabel("Category")
plt.ylabel("Value")

# Save the plot
plt.savefig("Week-2/visualizations/bar_chart.png")
# Display the plot
plt.show()