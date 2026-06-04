import arcade.color
from model.economy.colony import Colony
from model.economy.market import Market


class Nation:
    def __init__(self, name):
        self.name = name
        self.color = arcade.color.BLUE
        self.population = 1200000 # 1.2 million initial population, buildings each 10k, for 120 buildings
        self.gdp = 10000
        self.gdp_per_capita = 0

        self.colonies = []  # List of all colonies on planets
        self.solar_systems = []  # List of all owned solar systems
        self.capital = None

        self.treasury = 1000

    def on_monthly_update(self):
        pass
