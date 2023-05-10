import time
from avui.avui import Avui

def main():
    # Initialize Avui
    ui = Avui()

    # Create a window with tags
    ui.add_window(10, 50, 1, 1, "main")

    # Add some text to the window
    ui.wprint(1, 1, "Hello, welcome to the Avui demo!", "main")

    # Create a second window with tags
    ui.add_window(10, 50, 12, 1, "second")

    # Add text to the second window
    ui.wprint(1, 1, "This is the second window!", "second")

    # Update and show the main window
    main_win = ui.get_win_by_tag("main")[0]
    main_win.window_title("Main Window")
    ui.show_win(main_win)

    # Wait for 3 seconds
    time.sleep(3)

    # Hide the main window
    ui.hide_win(main_win)

    # Update and show the second window
    second_win = ui.get_win_by_tag("second")[0]
    second_win.window_title("Second Window")
    ui.show_win(second_win)

    # Wait for 3 seconds
    time.sleep(3)

    # Hide the second window and show the main window again
    ui.hide_win(second_win)
    ui.show_win(main_win)

    # Wait for 3 seconds
    time.sleep(3)

    # Finalize the UI and exit
    ui.finalize()


if __name__ == "__main__":
    main()
