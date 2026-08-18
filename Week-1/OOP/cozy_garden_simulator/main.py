from plant import Plant
from flower import Flower
from vegetable import Vegetable
from garden import Garden
from weather import Weather


garden = Garden()

rose = Flower("Rose", 3, "Red")
carrot = Vegetable("Carrot", 4, 5)

garden.add_plant(rose)
garden.add_plant(carrot)

weather = Weather("Sunny")
weather.display()

garden.water_all()
garden.grow_all()

garden.show_garden()