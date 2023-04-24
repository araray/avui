import sys
import curses

from curses import panel
from . import windows


class Avui:
    """
    Avui: A class to create and manage a user interface using the curses library.
    """

    def __init__(self):
        self.stdscr = None
        self.windows = []
        self.bgcolor = curses.COLOR_BLUE
        self.fgcolor = curses.COLOR_WHITE
        ncurses_version = curses.ncurses_version
        self.conf = {
            'NCURSES_VERSION': f"{ncurses_version.major}.{ncurses_version.minor}",
            'COLOR_DEPTH': 0
        }
        self.debug = ''
        self.initialize()

    def initialize(self):
        """
        Initialize the curses library and configure the terminal settings.
        """
        self.stdscr = curses.initscr()
        curses.cbreak()
        curses.noecho()
        curses.nonl()
        curses.curs_set(0)
        if not curses.can_change_color():
            self.finalize()
            print('This tool needs to be able to change terminal colors!')
            sys.exit(1)
        if sys.version_info.major == 3:
            if sys.version_info.minor >= 10:
                if float(self.conf['NCURSES_VERSION']) >= 6.1:
                    if curses.has_extended_color_support():
                        self.conf['COLOR_DEPTH'] = 256
            elif sys.version_info.minor >= 8:
                if curses.has_colors():
                    self.conf['COLOR_DEPTH'] = 16
                else:
                    self.conf['COLOR_DEPTH'] = 0
        curses.start_color()
        curses.init_pair(1, self.fgcolor, self.bgcolor)
        self.stdscr.bkgd(' ', curses.color_pair(1))
        self.stdscr.keypad(True)
        self.refresh(self.stdscr)
        self.max_y, self.max_x = self.get_max_yx(self.stdscr)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW)
        self.msg_type = {
            'ALERT': curses.color_pair(3) | curses.A_BLINK | curses.A_BOLD
        }

    def finalize(self):
        """
        Finalize the curses library and restore the terminal settings.
        """
        self.stdscr.clear()
        self.stdscr.keypad(False)
        curses.echo()
        curses.nl()
        curses.noraw()
        curses.nocbreak()
        curses.endwin()

    def refresh(self, target):
        """
        Refresh the target window or panel.
        """
        panel.update_panels()
        target.refresh()

    def add_window(self, dim_y, dim_x, pos_y, pos_x, *tags):
        """
        Add a new window to the interface with the specified dimensions, position, and tags.
        """
        win = windows.Windows()
        win.new_window(dim_y, dim_x, pos_y, pos_x, *tags)
        self.windows.append(win)
        self.refresh(win.cwin)

    def get_win_by_tag(self, tag):
        """
        Get a list of windows by their tag.
        """
        wins = []
        for win in self.windows:
            if tag in win.tags:
                wins.append(win)
                continue
        return wins

    def get_max_yx(self, target):
        """
        Get the maximum Y and X coordinates of the target window or panel.
        """
        return target.getmaxyx()

    def wprint(self, pos_y, pos_x, text, *tags):
        """
        Print text at the specified position in windows with the given tags.
        """
        for win in self.windows:
            for tag in tags:
                if tag in win.tags:
                    if len(text) + pos_x >= win.dim.x:
                        win.cwin.addstr(1, 1, f'{win.dim.x}')
                    else:
                        win.cwin.addstr(pos_y, pos_x, text)
                    self.refresh(win.cwin)
                    win.get_window_contents()
                    break

    def hide_win(self, win):
        """
        Hide the specified window.
        """
        win.hide()
        self.refresh(self.stdscr)

    def show_win(self, win):
        """
        Show the specified window.
        """
        win.show()
        self.refresh(self.stdscr)

    def move_win(self, win, new_y, new_x):
        """
        Move the specified window to the new Y and X coordinates.
        """
        win.move_window(new_y, new_x)
        self.refresh(self.stdscr)

    def add_n_windows(self, N, Y=0, X=0, *tags):
        """
        Add N windows to the interface, evenly spaced, with optional tags.
        """
        spacer = 1
        win_width = int((self.max_x - N * spacer) / N)
        win_height = int((self.max_y - N * spacer) / N)
        pos_x = X
        pos_y = Y
        for i in range(N):
            self.add_window(win_height, win_width, pos_y, pos_x, *tags)
            pos_x += win_width + spacer

