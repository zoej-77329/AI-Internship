# ------------------------------------------
# 1. Basic function
# ------------------------------------------

def greet():
    print("Welcome to the Garden Simulator!")


greet()


# ------------------------------------------
# 2. Function with a parameter
# ------------------------------------------

def greet_user(name):
    print(f"Hello, {name}!")


greet_user("Ayesha")
greet_user("Sara")


# ------------------------------------------
# 3. Multiple parameters
# ------------------------------------------

def add_numbers(a, b):
    print("Sum:", a + b)


add_numbers(10, 5)


# ------------------------------------------
# 4. Function with a return value
# ------------------------------------------

def calculate_area(length, width):
    area = length * width
    return area


garden_area = calculate_area(10, 5)

print("Garden area:", garden_area)


# ------------------------------------------
# 5. Function returning a calculated value
# ------------------------------------------

def calculate_water_level(current_level, amount):
    new_level = current_level + amount

    if new_level > 100:
        new_level = 100

    return new_level


water_level = calculate_water_level(70, 40)

print("New water level:", water_level)


# ------------------------------------------
# 6. Function with a condition
# ------------------------------------------

def check_plant_status(growth, required_growth):
    if growth >= required_growth:
        return "Plant is ready."
    else:
        return "Plant is still growing."


status = check_plant_status(5, 5)

print(status)


# ------------------------------------------
# 7. Function with a list
# ------------------------------------------

def display_plants(plants):
    print("\nPlants in the garden:")

    for plant in plants:
        print("-", plant)


plants = ["Rose", "Sunflower", "Tulip"]

display_plants(plants)