from imgui_bundle import imgui, immapp, ImVec2

class GrandStrategyUI:
    def __init__(self):
        # Mock State - normally managed by data containers via a Mediator
        self.treasury = 1450.50
        self.tax_rate = 15.0
        self.active_tab = "Overview"
        self.selected_province = "Livonia"
        self.show_details = True

    def draw_ui(self):
        """Main loop execution frame."""
        #self._setup_style()
        self._draw_top_bar()
        self._draw_left_sidebar()
        
        if self.show_details:
            self._draw_province_view()

    def _setup_style(self):
        """Sets up a dark, moody sci-fi/historical theme matching grand strategy games."""
        style = imgui.get_style()
        # Rounded tabs and windows look cleaner
        style.window_rounding = 4.0
        style.frame_rounding = 3.0
        
        # Subtle theme color adjustment example
        #colors = imgui.style.colors
        #colors[imgui.Col.window_bg] = imgui.ImColor(15, 20, 25, 240).to_im_vec4() # Deep slate/navy
        #colors[imgui.Col.header] = imgui.ImColor(40, 60, 80, 255).to_im_vec4()

    def _draw_top_bar(self):
        """Persistent global tracker across the top of the screen."""
        # Lock window to top, spanning full width
        io = imgui.get_io()
        imgui.set_next_window_pos(ImVec2(0, 0))
        imgui.set_next_window_size(ImVec2(io.display_size.x, 40))
        
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
        imgui.text(f" Selected: {self.selected_province}")
        
        # Align time/speed controls to the far right
        imgui.same_line(io.display_size.x - 120)
        imgui.text("2230.05.30 [||]")
        
        imgui.end()

    def _draw_left_sidebar(self):
        """Vertical dashboard control menu."""
        imgui.set_next_window_pos(ImVec2(0, 40))
        io = imgui.get_io()
        imgui.set_next_window_size(ImVec2(220, io.display_size.y - 40))
        
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
            if is_selected:
                #imgui.push_style_color(imgui.Col.button, imgui.ImColor(30, 80, 150).to_im_vec4())
                pass
            
            if imgui.button(tab, ImVec2(200, 35)):
                self.active_tab = tab
                
            if is_selected:
                #imgui.pop_style_color()
                pass

        imgui.end()

    def _draw_province_view(self):
        """Contextual data viewer resembling Victoria 3 pop systems."""
        # Floating window context
        imgui.set_next_window_pos(ImVec2(240, 60), imgui.Cond_.first_use_ever)
        imgui.set_next_window_size(ImVec2(400, 500), imgui.Cond_.first_use_ever)
        
        opened, self.show_details = imgui.begin("Province View", self.show_details)
        if opened:
            imgui.text(f"Region: {self.selected_province}")
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

# Run application using ImmApp runner
ui_instance = GrandStrategyUI()
#immapp.run(
#    gui_function=ui_instance.draw_ui, 
#    window_title="Project Grand Strategy", 
#    window_size=(1280, 720)
#)