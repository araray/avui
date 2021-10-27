import curses
import primitives

from curses import panel

class windows():
    dim = None
    pos = None
    tags = []
    cwin = None
    autorefresh = False
    lines_contents = []
    line_top = ''
    line_bot = ''
    panel = None

    def __init__(self):
        self.dim = primitives.rectangle()
        self.pos = primitives.coordinates()
        self.tags = []

    def new_window(self, dim_y, dim_x, pos_y, pos_x, *tags):
        self.dim.dimension(dim_x, dim_y)
        self.pos.place(pos_x, pos_y)
        win = curses.newwin(self.dim.y, self.dim.x, self.pos.y, self.pos.x)
        win.border(0,0,0,0)
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
        self.tags.append(tag)

    def highlight_window(self):
        self.cwin.bkgd(' ', curses.color_pair(0) | curses.A_REVERSE)

    def top_bar_info(self, info = '*', attrs = curses.A_BOLD):
        self.cwin.addstr(0, 0, f'[{info}]', attrs)

    def status_bar_info(self):
        pass

    def hide(self):
        self.panel.hide()

    def show(self):
        self.panel.show()

    def window_title(self, title):
        title = f' {title} '
        text = ''
        text += self.line_top[0:3]
        text += title
        text += self.line_top[len(title) + 3 : len(self.line_top)]
        self.cwin.addstr(0, 3, text)
        self.update_window_contents()

    def get_window_contents(self):
        lines = []
        for y in range(self.dim.y):
            buffer = ''
            for x in range(self.dim.x):
                char = bytes(self.cwin.inch(y, x))[8:15]
                buffer += char.decode('utf-8')
            lines.append(buffer.rstrip('\x00'))
        return lines

    def update_window_contents(self):
        self.lines_contents.clear()
        self.lines_contents = self.get_window_contents()
        self.line_top = self.lines_contents[0]
        self.line_bot = self.lines_contents[self.dim.y - 1]

    def move_window(self, new_y, new_x):
        self.cwin.mvwin(new_y, new_x)
