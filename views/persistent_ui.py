import arcade
from views.assets import assets
from imgui_bundle import imgui, implot
from imgui_bundle.python_backends import pyglet_backend

from imgui_bundle.python_backends import pyglet_backend


class PersistentUI:
    """Primary GUI controller for all IMGUI HUD data"""
    def __init__(self, game_model):
        self.game_model = game_model
        self.asset_manager = assets
        self.player_nation = None

        imgui.create_context()
        self.imgui_renderer = pyglet_backend.create_renderer(self)

    def set_player_nation(self, nation):
        self.player_nation = nation
        self.top_bar.player_nation = nation

    def draw(self):
        # 2. CONSTRUCT THE IMGUI FRAME
        imgui.new_frame()

        # Render our custom Stellaris panel function
        self.draw_stellaris_colony_panel()

        # 3. RENDER IMGUI ON TOP
        imgui.render()
        self.imgui_renderer.render(imgui.get_draw_data())

    def draw_stellaris_colony_panel(self):
        """ImGui code creating a locked left-hand panel matching Stellaris"""
        
        # Lock the window to the left side of the screen, spanning full height
        imgui.set_next_window_pos((0, 0))
        imgui.set_next_window_size((400, self.height))
        

        # Enforce a flat, non-movable application layout style
        window_flags = (imgui.WindowFlags_.no_title_bar | 
                        imgui.WindowFlags_.no_resize | 
                        imgui.WindowFlags_.no_move | 
                        imgui.WindowFlags_.no_collapse |
                        imgui.WindowFlags_.no_bring_to_front_on_focus)

        # Begin drawing the window
        imgui.begin("Colony Panel", flags=window_flags)

        # --- PANEL HEADER ---
        imgui.text_disabled(self.colony.type.upper())
        #imgui.push_font(imgui.get_io().fonts.fonts[0]) # Use standard font but bigger scale if desired
        imgui.text(f" Planet: {self.colony.name}")
        #imgui.pop_font()
        imgui.separator()

        # --- QUICK STATS GRID (Using Columns) ---
        imgui.columns(2, "stats_grid", borders=False)
        imgui.text(f"Pops: {self.colony.pops}")
        imgui.text(f"Stability: {self.colony.stability}%")
        imgui.next_column()
        imgui.text(f"Energy: +{self.colony.energy_income}/mo")
        imgui.text(f"Alloys: +{self.colony.alloy_income}/mo")
        imgui.columns(1) # Reset columns back to normal document flow
        imgui.separator()

        # --- STELLARIS-STYLE TAB BAR ---
        if imgui.begin_tab_bar("ColonyViewTabs"):
            
            # TAB 1: STRUCTURES
            if imgui.begin_tab_item("Structures")[0]:
                imgui.spacing()
                imgui.text("Planet Infrastructure")
                
                # Create a scrollable list bounding box for buildings
                # width=0 fills available space, height=-100 leaves room for a footer
                imgui.begin_child("BuildingScrollRegion", size=(0, -100))
                
                for index, building in enumerate(self.colony.buildings):
                    imgui.push_id(f"build_{index}") # Unique ID for widget interactions inside a loop
                    
                    # Horizontal Layout: [Icon] Name (Output) ........ [Button]
                    imgui.text_colored((0.3, 0.8, 1.0, 1.0), building.icon) # Colorized text code
                    imgui.same_line()
                    imgui.text(f"{building.name}")
                    imgui.same_line()
                    imgui.text_disabled(f"({building.output})")
                    
                    # Push button to the far right side of the row
                    imgui.same_line(imgui.get_window_width() - 90)
                    if imgui.button("Upgrade"):
                        self.selected_building_log = f"Upgraded {building.name}! Cost: 50 Alloys."
                        self.colony.alloy_income += 2 # Alter real game variables instantly!
                        
                    imgui.pop_id()
                    imgui.separator()
                    
                imgui.end_child()
                imgui.end_tab_item()

            # TAB 2: POPULATIONS
            if imgui.begin_tab_item("Populations")[0]:
                imgui.spacing()
                imgui.text("Demographics & Jobs")
                imgui.text(f"Total Working Pops: {self.colony.pops}")
                imgui.bullet_text("Rulers: 2 Pops (100% Happiness)")
                imgui.bullet_text("Specialists: 10 Pops (85% Happiness)")
                imgui.bullet_text("Workers: 16 Pops (70% Happiness)")
                imgui.end_tab_item()

        imgui.end_tab_bar()

        # --- FOOTER PANEL ---
        # Fixed tracking at the bottom of our left sidebar menu
        imgui.set_cursor_pos((10, self.height - 80))
        imgui.separator()
        imgui.text_wrapped(f"Action Log:\n{self.selected_building_log}")

        imgui.end() # Close "Colony Panel"


    #TODO: probably refactor these 3 "show menu" functions into 1, possibly with kwargs
    def show_planet_menu(self, colony):
        self.planet_menu.open_window(colony)

    def show_market_gui(self):
        self.market_gui.open_window(self.player_nation.national_market)

    def show_building_gui(self, building):
        self.building_gui.open_window(building)

class GalaxyStarLabel:
    def __init__(self, body, text_sprite_list, bg_sprite_list):
        self.body = body
        self.color = (arcade.color.DARK_GREEN)
        self.text = arcade.create_text_sprite(
            text=body.name,
        )
        self.text.center_x = body.x
        self.text.center_y = body.y - 40

        self.background = arcade.SpriteSolidColor(
            width=self.text.width + 10,
            height=self.text.height + 4,
            color=self.color,
            center_x=self.text.center_x,
            center_y=self.text.center_y,
        )
        bg_sprite_list.append(self.background)
        text_sprite_list.append(self.text)

    def update(self, camera_zoom):
        scale_factor = 1 / camera_zoom
        self.background.scale = scale_factor
        self.text.scale = scale_factor

# Solar system UI elements and sprites
class CelestialBodySprite(arcade.SpriteCircle):
    def __init__(self, body):
        super().__init__(body.size, body.color)
        self.model_reference = body

    def update(self, delta_time: float = 1/60):
        body_pos = self.model_reference.get_position()
        self.center_x = body_pos[0]
        self.center_y = body_pos[1]

class CelestialBodyLabel:
    def __init__(self, body, spritelist):
        self.body = body
        self.color = (arcade.color.CHARCOAL)
        self.text = arcade.Text(
            text=body.name,
            #font_size=16,
            x=0,
            y=0,
        )
        texture_size = (
            int(self.text.content_width + 20), 
            int(self.text.content_height + 10)
        )
        self.text.anchor_x = "center"
        self.text.anchor_y = "center"
        self.text.x = texture_size[0] / 2
        self.text.y = texture_size[1] / 2 
        self.texture = arcade.Texture.create_empty(body.name, size=texture_size)
        
        self.sprite = arcade.Sprite(
            self.texture,
            center_x=body.x,
            center_y=body.y - 40,
        )

        spritelist.append(self.sprite)
        with spritelist.atlas.render_into(self.texture) as fbo:
            fbo.clear(color=self.color)
            arcade.draw_lbwh_rectangle_outline(
                left=0,
                bottom=0,
                width=texture_size[0],
                height=texture_size[1],
                color=arcade.color.WHITE,
                border_width=4,
            )
            self.text.draw()

    def update(self, camera_zoom):
        scale_factor = 1 / camera_zoom
        self.sprite.scale = scale_factor
        self.sprite.center_y = self.body.y - (40 * scale_factor)


class PlanetLabel(CelestialBodyLabel):
    def __init__(self, body, spritelist):
        self.body = body
        position = body.get_position()
        body.x = position[0]
        body.y = position[1]
        super().__init__(body, spritelist)

import math

def draw_dashed_circle_outline(center_x, center_y, radius, color, border_width=2, num_dashes=100, dash_fraction=0.5):
    angle_per_dash = 2 * math.pi / num_dashes
    dash_angle = angle_per_dash * dash_fraction
    for i in range(num_dashes):
        start_angle = i * angle_per_dash
        end_angle = start_angle + dash_angle
        x1 = center_x + radius * math.cos(start_angle)
        y1 = center_y + radius * math.sin(start_angle)
        x2 = center_x + radius * math.cos(end_angle)
        y2 = center_y + radius * math.sin(end_angle)
        arcade.draw_line(x1, y1, x2, y2, color, border_width)
