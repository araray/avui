# Avui

Avui is a Python library for creating text-based user interfaces (TUIs) using the `curses` library. With a simple and easy-to-use API, you can create windows, display text, and manage tags for your TUI applications.

## Features

- Simple API for creating windows and displaying text
- Window tagging for easy management
- Customizable window titles
- Window hiding and showing
- PEP 8 compliant code

## Installation

To use Avui, simply clone this repository or copy the `avui` folder into your project directory.

## Usage

Here is a simple example demonstrating how to create a basic TUI with Avui:

```python
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
```

## Documentation

Avui uses the `curses` library to manage TUI elements. Please refer to the [Python curses documentation](https://docs.python.org/3/library/curses.html) for more information on how the `curses` library works.

For Avui-specific documentation, refer to the docstrings and comments provided in the source code. The main classes you will interact with are:

- `Avui`: The main class for managing your TUI application. Use it to create windows, display text, and manage tags.
- `Windows`: A class representing a window in your TUI. Use it to update and manage the window's content and appearance.

## License

This project is available under the [BSD-3-Clause License](https://opensource.org/licenses/BSD-3-Clause).

