import win32gui
import win32process
import win32con
import logging

logger = logging.getLogger("FishBot.Window")


def list_windows():
    logger.debug("Listing all visible windows")
    result = []

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                result.append((hwnd, title, pid))

    win32gui.EnumWindows(callback, None)
    logger.debug(f"Found {len(result)} windows")
    return result


def focus_window(hwnd):
    logger.info(f"Focusing window (hwnd={hwnd})")
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
    logger.debug("Window focused successfully")


def get_window_rect(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    rect = {
        "left": left,
        "top": top,
        "width": right - left,
        "height": bottom - top
    }
    logger.debug(f"Window rect for hwnd={hwnd}: {rect}")
    return rect
