import avui
import curses
import time

a = avui.avui()
time.sleep(1)

x = a.max_x
y = a.max_y

a.add_window(10,30,6,4,'a','c')
a.windows[0].autorefresh = True
a.add_window(3,x,y-3,0,'b','c')
a.windows[0].highlight_window()
a.windows[0].window_title('Test TITLE')
a.wprint(1, 3, ' Aaiv ', 'a')
a.wprint(3, 3, 'Test text for testing!', 'a')
a.windows[0].top_bar_info('*', a.msg_type['ALERT'])
a.add_n_windows(6, 0, 0, 'cont')
a.wprint(1, 3, ' Docker ', 'cont')
a.stdscr.getch()
map = a.win_map
a.finalize()
