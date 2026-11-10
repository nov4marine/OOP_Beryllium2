import arcade
from model.model import GameModel
from views.galaxy_view import GalaxyView
# from views.solar_system_view import SolarSystemView
from views.pergui import PerGUI


class MyGame:
    def __init__(self):
        self.game_model = GameModel()  # Central simulation

        self.width = 1920
        self.height = 1080
        self.title = "Beryllium"
        self.window = arcade.Window(
            width=self.width,
            height=self.height,
            title=self.title,
        )

        print(f"Default texture atlas size: {self.window.ctx.default_atlas.width}x{self.window.ctx.default_atlas.height}")
        self.window.ctx.default_atlas.resize((8192, 8192))

        # --- Resources to load ---
        self.game_model.initialize_new_game()
        self.pergui = PerGUI(self.game_model)

        self.galaxy_view = GalaxyView(self.game_model, self.pergui)
        self.main_menu_view = None
        
        self.window.show_view(self.galaxy_view)



if __name__ == "__main__":
    game = MyGame()
    arcade.run()

"""
TODO:
1. go over pergui and decide what to switch to imgui and what to keep arcade sprites.
2. Refactor managers back into OOP format (called mediator or federated?)
3. Rework basic resources to be more like prosperous universe than Stellaris?

1. go over model from the top down to make sure everything initializes correctly (ignore within colony for now)
1.5 rewrite calendar to sort thru who needs what type of update, and for the gui
2. do step 2 but within colony
3. refactor buildings and other systems back into OOP from ECS
4. Asses the current state of the pergui
5. refactor pergui and add onto it for a very minimal colony gui, use it to confirm data is working as expected.

1. Refactor galaxy to not generate world upon spawn, instead do so when instructed.
"""