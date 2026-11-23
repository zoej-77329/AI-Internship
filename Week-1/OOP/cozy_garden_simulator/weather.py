class Weather:
    def __init__(self, condition):
        self.condition = condition

    def display(self):
        print(f"Today's weather: {self.condition}")