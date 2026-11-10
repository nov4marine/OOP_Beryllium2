import arcade
import random
import numpy as np
from imgui_bundle import imgui, implot, ImVec2
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


class StellarisClone(arcade.Window):
    def __init__(self):
        super().__init__(1920, 1080, "Economy Simulator", resizable=True)
        
        self.colony = ColonyData
        self.active_tab = None
        self.tax_rate = 0.15

        # 1. Setup ImGui
        imgui.create_context()
        implot.create_context() # Important: ImPlot needs its own context!
        self.imgui_renderer = pyglet_backend.create_renderer(self)

    def on_draw(self):
        self.clear()
        
        # --- Draw Game World (The "Map") ---
        arcade.draw_text("Space Map (Arcade)", 400, 350, arcade.color.DARK_GRAY, 20)
        arcade.draw_circle_outline(500, 350, 200, arcade.color.BATTLESHIP_GREY)

        # --- Draw UI (ImGui) ---
        imgui.new_frame()
            
        self._draw_top_bar()
        self._draw_left_sidebar()
        self._draw_right_ledger()
        
        self._draw_province_view()

        #imgui.end()
        imgui.render()
        self.imgui_renderer.render(imgui.get_draw_data())

    def _draw_top_bar(self):
        """Persistent global tracker across the top of the screen."""
        # Lock window to top, spanning full width
        io = imgui.get_io()
        imgui.set_next_window_pos(ImVec2(0, 0))
        imgui.set_next_window_size(ImVec2(io.display_size.x, 50))
        
        # Flags to make it a seamless panel
        flags = (imgui.WindowFlags_.no_title_bar | 
                 imgui.WindowFlags_.no_resize | 
                 imgui.WindowFlags_.no_move | 
                 imgui.WindowFlags_.no_scrollbar)
        
        imgui.begin("##TopBar", None, flags)
        
        # Format strings to style like resource counters
        #imgui.text_colored(imgui.ImColor(255, 215, 0).to_im_vec4(), f" Gold: {self.treasury:,.2f}")
        imgui.same_line(spacing=20.0)
        imgui.text(" Stability: +2")
        imgui.same_line(spacing=20.0)
        #imgui.text(f" Selected: {self.selected_province}")
        
        # Align time/speed controls to the far right
        imgui.same_line(io.display_size.x - 120)
        imgui.text("2230.05.30 [||]")
        
        imgui.end()

    def _draw_left_sidebar(self):
        """Vertical dashboard control menu."""
        io = imgui.get_io()
        imgui.set_next_window_pos(ImVec2(0, 50))
        imgui.set_next_window_size(ImVec2(200, 600))
        
        flags = (imgui.WindowFlags_.no_title_bar | 
                 imgui.WindowFlags_.no_resize | 
                 imgui.WindowFlags_.no_move)
        
        imgui.begin("##LeftSidebar", None, flags)
        
        imgui.text_disabled("EMPIRE INTERFACE")
        imgui.separator()
        imgui.spacing()

        # Navigation Tabs
        tabs = ["Overview", "Economy", "Politics", "Military"]
        for tab in tabs:
            # Highlight selected button
            is_selected = (self.active_tab == tab)
            
            if imgui.button(tab, ImVec2(180, 35)):
                self.active_tab = tab

        imgui.end()


    def _draw_right_ledger(self):
        # Dummy data to simulate your game state
        planets = [f"Planet {char}" for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        fleets = ["1st Strike Armada", "2nd Corvette Flotilla", "Science Vessel Vanguard"]

        # 1. Lock the main Ledger window to the right side of the screen
        # (In your actual game, you'd set this position/size to fit your HUD)
        imgui.set_next_window_pos((1700, 200), imgui.Cond_.always)
        imgui.set_next_window_size((220, 560), imgui.Cond_.always)
        
        # Start the main Ledger container
        imgui.begin("Outliner", None, imgui.WindowFlags_.no_collapse | imgui.WindowFlags_.no_resize)
        
        imgui.text_colored(imgui.ImVec4(0.3, 0.8, 1, 1), "GALAXY EMPIRE LEDGER")
        imgui.separator()
        
        # 2. CREATE THE SCROLLABLE REGION (The Child Window)
        # Arguments: ("UniqueName", (width, height), border_bool)
        # Using 0 for width means "fill the parent window width".
        # Using 0 for height means "fill the remaining space".
        if imgui.begin_child("LedgerScrollRegion", (0, 0), True):
            
            # --- SECTION: PLANETS ---
            if imgui.collapsing_header("Planets"):
                for planet in planets:
                    # Selectable acts like a button that spans the full row
                    if imgui.selectable(f"🌍 {planet}", False)[0]:
                        print(f"Camera panning to {planet}...") 
                        # Here you would set self.selected_object = planet
                        
            imgui.spacing()
            
            # --- SECTION: FLEETS ---
            if imgui.collapsing_header("Fleets"):
                for fleet in fleets:
                    if imgui.selectable(f"🚀 {fleet}", False)[0]:
                        print(f"Selecting {fleet}...")

            # Always end the child window if begin_child returned True
            imgui.end_child()

        # End the main window
        imgui.end()

    def _draw_province_view(self):
        """Contextual data viewer resembling Victoria 3 pop systems."""
        # Floating window context
        imgui.set_next_window_pos(ImVec2(240, 60), imgui.Cond_.first_use_ever)
        imgui.set_next_window_size(ImVec2(400, 500), imgui.Cond_.first_use_ever)
        
        opened, self.show_details = imgui.begin("Province View")
        if opened:
            imgui.text("Region: selected_province")
            imgui.separator()
            
            # Using ImGui's heavy-duty Table API for Pop details / economic chains
            if imgui.begin_table("PopTable", 3, imgui.TableFlags_.borders | imgui.TableFlags_.row_bg):
                imgui.table_setup_column("Demographic")
                imgui.table_setup_column("Size")
                imgui.table_setup_column("Workforce")
                imgui.table_headers_row()
                
                # Pop Sample Row 1
                imgui.table_next_row()
                imgui.table_next_column(); imgui.text("Laborers")
                imgui.table_next_column(); imgui.text("142,000")
                imgui.table_next_column(); imgui.text("Iron Mines")
                
                # Pop Sample Row 2
                imgui.table_next_row()
                imgui.table_next_column(); imgui.text("Clerks")
                imgui.table_next_column(); imgui.text("12,500")
                imgui.table_next_column(); imgui.text("Administration")
                
                imgui.end_table()
            
            imgui.spacing()
            imgui.separator()
            imgui.spacing()
            
            # Interactive State Management Example
            imgui.text("Regional Adjustments")
            changed, self.tax_rate = imgui.slider_float("Local Tax %", self.tax_rate, 0.0, 100.0, "%.1f%%")
            if changed:
                # This is where your code handles downstream simulation updates via a Mediator or registry
                pass
                
        imgui.end()


if __name__ == "__main__":
    game = StellarisClone()
    arcade.run()