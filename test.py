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
a.add_n_windows(6, 0, 0, 'cont')
a.windows[0].highlight_window()
a.windows[0].window_title('Title')
a.wprint(1, 3, 'Some text', 'a')
a.wprint(3, 3, 'Test text for testing!', 'a')
a.windows[0].top_bar_info('*', a.msg_type['ALERT'])
a.wprint(1, 3, ' Docker ', 'cont')
time.sleep(2)
for w in a.get_win_by_tag('a'):
    w.panel.top()
    a.refresh(w.cwin)
    time.sleep(2)
    a.hide_win(w)
    time.sleep(2)
    a.move_win(w, 20,20)
    a.show_win(w)

a.stdscr.getch()
a.finalize()
