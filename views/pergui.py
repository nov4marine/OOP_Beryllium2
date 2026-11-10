import arcade
from views.assets import assets
from imgui_bundle import imgui, implot, immapp, ImVec2
from imgui_bundle.python_backends import pyglet_backend


class PerGUI:
    def __init__(self, model):
        self.model = model
        self.nation = model.player_nation
        self.active_tab = None

        # 1. Setup ImGui
        imgui.create_context()
        implot.create_context()  # Important: ImPlot needs its own context!
        self.imgui_renderer = pyglet_backend.create_renderer(self)

    def draw(self):
        # --- Draw UI (ImGui) ---
        imgui.new_frame()

        self._draw_top_bar()
        self._draw_left_sidebar()
        self._draw_right_ledger()

        self._draw_province_view()

        # imgui.end()
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
        # imgui.text_colored(imgui.ImColor(255, 215, 0).to_im_vec4(), f" Gold: {self.treasury:,.2f}")
        imgui.same_line(spacing=20.0)
        imgui.text(" Stability: +2")
        imgui.same_line(spacing=20.0)

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
                imgui.table_next_column();
                imgui.text("Laborers")
                imgui.table_next_column();
                imgui.text("142,000")
                imgui.table_next_column();
                imgui.text("Iron Mines")

                # Pop Sample Row 2
                imgui.table_next_row()
                imgui.table_next_column();
                imgui.text("Clerks")
                imgui.table_next_column();
                imgui.text("12,500")
                imgui.table_next_column();
                imgui.text("Administration")

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
