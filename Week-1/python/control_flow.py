# ------------------------------------------
# 1. if, elif, else
# ------------------------------------------

age = 21

if age >= 18:
    print("You are an adult.")
elif age >= 13:
    print("You are a teenager.")
else:
    print("You are a child.")


# ------------------------------------------
# 2. Checking a number
# ------------------------------------------

number = 10

if number > 0:
    print("The number is positive.")
elif number < 0:
    print("The number is negative.")
else:
    print("The number is zero.")


# ------------------------------------------
# 3. for loop
# ------------------------------------------

print("\nNumbers from 1 to 5:")

for i in range(1, 6):
    print(i)


# ------------------------------------------
# 4. for loop with a list
# ------------------------------------------

plants = ["Rose", "Sunflower", "Tulip", "Jasmine"]

print("\nPlants:")

for plant in plants:
    print(plant)


# ------------------------------------------
# 5. while loop
# ------------------------------------------

print("\nCounting using while loop:")

count = 1

while count <= 5:
    print(count)
    count += 1


# ------------------------------------------
# 6. Combining conditions and loops
# ------------------------------------------

print("\nEven numbers:")

for number in range(1, 11):
    if number % 2 == 0:
        print(number)