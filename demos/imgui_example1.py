import arcade
from imgui_bundle import imgui, implot
from imgui_bundle.python_backends import pyglet_backend 

# --- DUMMY GAME MODEL DATA ---
class ColonyBuilding:
    def __init__(self, name, icon, output):
        self.name = name
        self.icon = icon
        self.output = output

class ColonyData:
    def __init__(self):
        self.name = "Prime Nexus"
        self.type = "Continental World"
        self.pops = 28
        self.stability = 82
        self.energy_income = 45
        self.alloy_income = 12
        self.buildings = [
            ColonyBuilding("Energy Grid", "[E]", "+15 Energy"),
            ColonyBuilding("Alloy Mega-Forge", "[A]", "+10 Alloys"),
            ColonyBuilding("Research Lab", "[R]", "+6 Science"),
            ColonyBuilding("Hydroponics Farm", "[H]", "+8 Food"),
            ColonyBuilding("City District", "[C]", "+5 Housing"),
            ColonyBuilding("Mineral Purification Plant", "[M]", "+12 Minerals"),
            ColonyBuilding("Holotheater", "[F]", "+10 Amenities"),
        ]

# --- MAIN ARCADE VIEW ---
class StellarisGuiDemo(arcade.Window):
    def __init__(self):
        super().__init__(1280, 720, "Stellaris UI Demo", resizable=True)
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        
        # Initialize our dummy game data
        self.colony = ColonyData()
        self.selected_building_log = "Click an upgrade button..."

        # Initialize the ImGui Arcade Renderer
        imgui.create_context()
        self.imgui_renderer = pyglet_backend.create_renderer(self)

    def on_update(self, delta_time: float):
        # Fake running game updates here if needed
        pass

    def on_draw(self):
        self.clear()

        # 1. DRAW YOUR ARCADE GAME WORLD FIRST
        # This represents your galaxy map or solar system behind the UI
        arcade.draw_circle_filled(640, 360, 40, arcade.color.YELLOW) # A star
        arcade.draw_text("Galaxy Map Space (Arcade Canvas)", 500, 300, arcade.color.WHITE, 14)

        # 2. CONSTRUCT THE IMGUI FRAME
        imgui.new_frame()

        # Render our custom Stellaris panel function
        self.render_stellaris_colony_panel()

        # 3. RENDER IMGUI ON TOP
        imgui.render()
        self.imgui_renderer.render(imgui.get_draw_data())

    def render_stellaris_colony_panel(self):
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


    # --- CRITICAL INPUT HANDLING ---
    # Gating the mouse so clicking UI windows doesn't hit the map behind it
    def on_mouse_press(self, x, y, button, modifiers):
        if imgui.get_io().want_capture_mouse:
            return # ImGui handled it!
        
        # Normal arcade interactions go below here
        print(f"Arcade Canvas Clicked at coordinates: {x}, {y}")


if __name__ == "__main__":
    app = StellarisGuiDemo()
    arcade.run()