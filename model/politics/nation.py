import arcade.color
from model.economy.colony import Colony


class Nation:
    def __init__(self, name):
        self.name = name
        self.color = arcade.color.BLUE
        self.population = 0
        self.gdp = 0
        self.gdp_per_capita = 0

        self.colonies = []  # List of all colonies on planets
        self.solar_systems = []  # List of all owned solar systems
        self.capital = None

        self.treasury = 10_000

    def on_monthly_update(self):
        for colony in self.colonies: 
            colony.on_monthly_update()
            # Collect taxes
            # migration?
            
    
    
class NationTemplate:
    def __init__(self) -> None:
        self.population = 1_200_000 # 1.2 million initial population, buildings each 10k, for 120 buildings
