from plant import Plant


class Vegetable(Plant):
    def __init__(self, name, growth_time, sell_price):
        super().__init__(name, growth_time)
        self.sell_price = sell_price

    def harvest(self):
        if self.is_ready():
            print(f"{self.name} was harvested for ${self.sell_price}.")
            return self.sell_price

        print(f"{self.name} is not ready to harvest.")
        return 0