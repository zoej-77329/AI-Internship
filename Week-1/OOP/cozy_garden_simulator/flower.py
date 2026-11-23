from plant import Plant


class Flower(Plant):
    def __init__(self, name, growth_time, color):
        super().__init__(name, growth_time)
        self.color = color

    def bloom(self):
        if self.is_ready():
            print(f"{self.name} has bloomed!")
        else:
            print(f"{self.name} is still growing.")