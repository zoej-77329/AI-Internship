# ------------------------------------------
# 1. Lists
# ------------------------------------------

plants = ["Rose", "Sunflower", "Tulip"]

print("Plants:", plants)

# Access an element
print("First plant:", plants[0])

# Add an element
plants.append("Jasmine")

print("After adding a plant:", plants)

# Remove an element
plants.remove("Tulip")

print("After removing a plant:", plants)


# ------------------------------------------
# 2. Tuples
# ------------------------------------------

garden_location = (10, 20)

print("\nGarden location:", garden_location)
print("X coordinate:", garden_location[0])
print("Y coordinate:", garden_location[1])


# ------------------------------------------
# 3. Sets
# ------------------------------------------

plant_types = {"Flower", "Vegetable", "Flower", "Herb"}

print("\nPlant types:", plant_types)

# Add an item
plant_types.add("Fruit")

print("After adding Fruit:", plant_types)


# ------------------------------------------
# 4. Dictionaries
# ------------------------------------------

plant = {
    "name": "Rose",
    "type": "Flower",
    "water_level": 80,
    "growth_days": 5
}

print("\nPlant information:")
print(plant)

# Access dictionary values
print("Name:", plant["name"])
print("Type:", plant["type"])
print("Water level:", plant["water_level"])


# Update a value
plant["water_level"] = 100

print("Updated water level:", plant["water_level"])


# Add a new key
plant["color"] = "Red"

print("Updated plant:", plant)


# ------------------------------------------
# 5. Looping through a dictionary
# ------------------------------------------

print("\nPlant details:")

for key, value in plant.items():
    print(key, ":", value)