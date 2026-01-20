import win32gui
import win32process
import win32con

def list_windows():
    result = []

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                result.append((hwnd, title, pid))

    win32gui.EnumWindows(callback, None)
    return result


def focus_window(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)


def get_window_rect(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    return {
        "left": left,
        "top": top,
        "width": right - left,
        "height": bottom - top
    }
