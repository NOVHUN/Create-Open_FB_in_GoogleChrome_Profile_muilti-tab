import win32gui
import win32con
import win32api

# Function to get all visible windows
def get_visible_windows():
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            windows.append(hwnd)
        return True

    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

# Function to minimize all windows except the specified ones
def minimize_windows_except(except_windows):
    for hwnd in get_visible_windows():
        if hwnd not in except_windows:
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

# Function to arrange windows in a grid layout
def arrange_windows_in_grid(windows):
    num_tasks = len(windows)
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)

    # Calculate grid dimensions
    grid_cols = int(num_tasks**0.5)
    grid_rows = (num_tasks + grid_cols - 1) // grid_cols

    # Calculate grid cell dimensions
    cell_width = screen_width // grid_cols
    cell_height = screen_height // grid_rows

    # Arrange windows in grid layout
    for i, hwnd in enumerate(windows):
        col = i % grid_cols
        row = i // grid_cols
        left = col * cell_width
        top = row * cell_height
        right = min((col + 1) * cell_width, screen_width)
        bottom = min((row + 1) * cell_height, screen_height)
        win32gui.MoveWindow(hwnd, left, top, right - left, bottom - top, True)

# Example usage
if __name__ == "__main__":
    windows = get_visible_windows()
    minimize_windows_except(windows)
    arrange_windows_in_grid(windows)
