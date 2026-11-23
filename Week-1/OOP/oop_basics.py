#------------------------------------------
# -------Encapsulation Example-------
class Plant:
    def __init__(self, name, water_level):
        self.name = name
        self.__water_level = water_level

    def water(self):
        self.__water_level += 20

    def get_water_level(self):
        return self.__water_level


plant = Plant("Rose", 40)

plant.water()

print(plant.get_water_level())

#------------------------------------------ 
# -------Inheritance Example-------
class Plant:
    def __init__(self, name):
        self.name = name

    def grow(self):
        print(f"{self.name} is growing.")


class Flower(Plant):
    def bloom(self):
        print(f"{self.name} is blooming.")


class Vegetable(Plant):
    def harvest(self):
        print(f"{self.name} is ready to harvest.")


flower = Flower("Rose")
vegetable = Vegetable("Carrot")

flower.grow()
flower.bloom()

vegetable.grow()
vegetable.harvest()

#------------------------------------------
#------Polymorphism Example-------
class Plant:
    def __init__(self, name):
        self.name = name

    def describe(self):
        print(f"{self.name} is a plant.")


class Flower(Plant):
    def describe(self):
        print(f"{self.name} is a flower that can bloom.")


class Vegetable(Plant):
    def describe(self):
        print(f"{self.name} is a vegetable that can be harvested.")


plants = [
    Flower("Rose"),
    Vegetable("Carrot")
]

for plant in plants:
    plant.describe()