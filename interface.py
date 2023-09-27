import curses
import curses.panel

class UiElement:
    def draw(self):
        pass
    
    def hide(self):
        pass
    
    def show(self):
        pass

class UiWindow(UiElement):
    def __init__(self, height, width, start_y, start_x):
        self.window = curses.newwin(height, width, start_y, start_x)

    def draw_text(self, y, x, text, attribute=None):
        self.window.addstr(y, x, text, attribute)

    def draw_border(self):
        self.window.box()

    def set_color(self, fg, bg):
        curses.init_pair(1, fg, bg)
        self.window.bkgd(' ', curses.color_pair(1))

    def refresh(self):
        self.window.refresh()

    # ... Add more window-specific methods.

class UiPanel(UiElement):
    def __init__(self, ui_window):
        self.panel = curses.panel.new_panel(ui_window.window)
        
    def move_to_top(self):
        self.panel.top()
        
    def move_to_bottom(self):
        self.panel.bottom()

    # ... Add more panel-specific methods.

class UiInput:
    @staticmethod
    def get_key():
        return curses.getch()

    @staticmethod
    def get_mouse_event():
        return curses.getmouse()

    # ... Add more input-related methods.

class UiColor:
    def __init__(self):
        curses.start_color()

    @staticmethod
    def define_color_pair(number, fg, bg):
        curses.init_pair(number, fg, bg)

    @staticmethod
    def get_color_pair(number):
        return curses.color_pair(number)

    # ... Add more color-related methods.
