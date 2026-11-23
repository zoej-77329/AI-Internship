class Plant:
    def __init__(self, name, growth_time):
        self.name = name
        self.growth_time = growth_time
        self.current_growth = 0
        self.water_level = 50

    def water(self):
        self.water_level = min(100, self.water_level + 30)
        print(f"{self.name} was watered.")

    def grow(self):
        if self.water_level > 0:
            self.current_growth += 1
            self.water_level -= 10
            print(f"{self.name} grew by one day.")
        else:
            print(f"{self.name} needs water.")

    def is_ready(self):
        return self.current_growth >= self.growth_time

