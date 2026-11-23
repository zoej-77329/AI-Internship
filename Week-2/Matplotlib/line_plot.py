import matplotlib.pyplot as plt

# Data
months = ["Jan", "Feb", "Mar", "Apr", "May"]
sales = [120, 150, 140, 180, 200]

# Create line plot
plt.plot(months, sales)

# Add title and labels
plt.title("Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Sales")

# Save the plot
plt.savefig("Week-2/visualizations/line_plot.png")
# Display the plot
plt.show()