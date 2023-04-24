import curses

from bresenham import bresenham
from curses import panel
from .primitives import Rectangle, Coordinates


class Windows:
    """
    Windows: A class to manage windows using the curses library.
    """

    def __init__(self):
        self.dim = Rectangle()
        self.pos = Coordinates()
        self.tags = []
        self.cwin = None
        self.autorefresh = False
        self.lines_contents = []
        self.line_top = ''
        self.line_bot = ''
        self.panel = None

    def new_window(self, dim_y, dim_x, pos_y, pos_x, *tags):
        """
        Create a new window with the specified dimensions, position, and tags.
        """
        self.dim.dimension(dim_x, dim_y)
        self.pos.place(pos_x, pos_y)
        win = curses.newwin(self.dim.y, self.dim.x, self.pos.y, self.pos.x)
        win.border(0, 0, 0, 0)
        for tag in tags:
            self.tag_window(tag)
        self.cwin = win
        self.panel = panel.new_panel(self.cwin)
        self.panel.top()
        self.panel.show()
        panel.update_panels()
        self.cwin.immedok(self.autorefresh)
        self.update_window_contents()
        return win

    def tag_window(self, tag):
        """
        Add a tag to the window.
        """
        self.tags.append(tag)

    def highlight_window(self):
        """
        Highlight the window.
        """
        self.cwin.bkgd(' ', curses.color_pair(0) | curses.A_REVERSE)

    def top_bar_info(self, info='*', attrs=curses.A_BOLD):
        """
        Display the top bar information.
        """
        self.cwin.addstr(0, 0, f'[{info}]', attrs)

    def status_bar_info(self):
        """
        Display the status bar information.
        """
        pass

    def hide(self):
        """
        Hide the window.
        """
        self.panel.hide()

    def show(self):
        """
        Show the window.
        """
        self.panel.show()

    def window_title(self, title):
        """
        Set the window title.
        """
        title = f' {title} '
        text = ''
        text += self.line_top[0:3]
        text += title
        text += self.line_top[len(title) + 3: len(self.line_top)]
        self.cwin.addstr(0, 3, text)
        self.update_window_contents()

    def get_window_contents(self):
        """
        Get the contents of the window as a list of strings.
        """
        lines = []
        for y in range(self.dim.y):
            buffer = ''
            for x in range(self.dim.x):
                char = bytes(self.cwin.inch(y, x))[8:15]
                buffer += char.decode('utf-8')
            lines.append(buffer.rstrip('\x00'))
        return lines

    def update_window_contents(self):
        """
        Update the window's content.
        """
        self.lines_contents.clear()
        self.lines_contents = self.get_window_contents()
        self.line_top = self.lines_contents[0]
        self.line_bot = self.lines_contents[self.dim.y - 1]

    def move_window(self, new_y, new_x):
        """
        Move the window to the new Y and X coordinates.
        """
        self.cwin.mvwin(new_y, new_x)

    def draw_ellipse2(self, fill=True, character=" "):
        """Draw an ellipse within the window."""
        center_y, center_x = self.dim.y // 2, self.dim.x // 2
        ry, rx = center_y - 1, center_x - 1

        for y in range(self.dim.y):
            for x in range(self.dim.x):
                ellipse_value = ((y - center_y) / ry) ** 2 + ((x - center_x) / rx) ** 2
                if fill:
                    condition = ellipse_value <= 1
                else:
                    condition = 0.9 <= ellipse_value <= 1.1

                if condition:
                    self.cwin.addstr(y, x, character)
        self.update_window_contents()

    def draw_ellipse(self, fill=True, character=" "):
        """Draw an ellipse within the window."""
        center_y, center_x = self.dim.y // 2, self.dim.x // 2
        ry, rx = center_y - 1, center_x - 1

        def plot_ellipse_points(y, x):
            """Plot the corresponding ellipse points given a single point."""
            points = [
                (center_y + y, center_x + x),
                (center_y - y, center_x + x),
                (center_y + y, center_x - x),
                (center_y - y, center_x - x),
                (center_y + x, center_x + y),
                (center_y - x, center_x + y),
                (center_y + x, center_x - y),
                (center_y - x, center_x - y),
            ]

            for point_y, point_x in points:
                if 0 <= point_y < self.dim.y and 0 <= point_x < self.dim.x:
                    self.cwin.addstr(point_y, point_x, character)

        def draw_ellipse_border():
            """Draw the ellipse border using the Bresenham's algorithm."""
            y, x = ry, 0
            d = 4 * ry * ry * (1 - rx) + rx * rx
            plot_ellipse_points(y, x)

            while ry * ry * (2 * x + 1) < 2 * rx * rx * y:
                if d < 0:
                    d += 4 * ry * ry * (2 * x + 3)
                else:
                    d += 4 * (ry * ry * (2 * x + 3) + rx * rx * (1 - 2 * y))
                    y -= 1
                x += 1
                plot_ellipse_points(y, x)

            d = ry * ry * (x * x + 2 * x) + rx * rx * (y * y - 2 * y + 1) - 2 * rx * rx * ry * ry
            while y >= 0:
                if d < 0:
                    d += 4 * (rx * rx * (2 * y - 3) + ry * ry * (2 * x + 2))
                    x += 1
                else:
                    d += 4 * rx * rx * (1 - 2 * y)
                y -= 1
                plot_ellipse_points(y, x)


            if fill:
                for y in range(center_y - ry, center_y + ry + 1):
                    left_points = list(bresenham(center_x, center_y, center_x - rx, y))
                    right_points = list(bresenham(center_x, center_y, center_x + rx, y))
                    if left_points and right_points:
                        x1 = left_points[-1][0]
                        x2 = right_points[-1][0]
                        for x in range(x1, x2 + 1):
                            self.cwin.addstr(y, x, character)

            else:
                draw_ellipse_border()
        self.update_window_contents
