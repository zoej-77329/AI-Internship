class Garden:
    def __init__(self):
        self.plants = []

    def add_plant(self, plant):
        self.plants.append(plant)
        print(f"{plant.name} was added to the garden.")

    def water_all(self):
        for plant in self.plants:
            plant.water()

    def grow_all(self):
        for plant in self.plants:
            plant.grow()

    def show_garden(self):
        print("\n--- Garden ---")

        for plant in self.plants:
            print(
                f"{plant.name}: "
                f"Growth {plant.current_growth}/{plant.growth_time}, "
                f"Water {plant.water_level}%"
            )