import ctypes
import time
import logging

logger = logging.getLogger("FishBot.Input")

# Windows API
user32 = ctypes.windll.user32
SendInput = user32.SendInput
MapVirtualKey = user32.MapVirtualKeyW
PostMessageW = user32.PostMessageW
SendMessageW = user32.SendMessageW

# Constants
MAPVK_VK_TO_VSC = 0
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_KEYUP = 0x0002

# Window messages
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_CHAR = 0x0102

PUL = ctypes.POINTER(ctypes.c_ulong)

# Store target window handle
_target_hwnd = None

def set_target_window(hwnd):
    """Set the target window for PostMessage input method."""
    global _target_hwnd
    _target_hwnd = hwnd
    logger.info(f"Target window set to hwnd={hwnd}")

# Virtual key code mapping
VK_CODES = {
    "space": 0x20,
    "enter": 0x0D,
    "tab": 0x09,
    "esc": 0x1B,
    "backspace": 0x08,
    "shift": 0x10,
    "ctrl": 0x11,
    "alt": 0x12,
    "f1": 0x70, "f2": 0x71, "f3": 0x72, "f4": 0x73,
    "f5": 0x74, "f6": 0x75, "f7": 0x76, "f8": 0x77,
    "f9": 0x78, "f10": 0x79, "f11": 0x7A, "f12": 0x7B,
    "0": 0x30, "1": 0x31, "2": 0x32, "3": 0x33, "4": 0x34,
    "5": 0x35, "6": 0x36, "7": 0x37, "8": 0x38, "9": 0x39,
    "a": 0x41, "b": 0x42, "c": 0x43, "d": 0x44, "e": 0x45,
    "f": 0x46, "g": 0x47, "h": 0x48, "i": 0x49, "j": 0x4A,
    "k": 0x4B, "l": 0x4C, "m": 0x4D, "n": 0x4E, "o": 0x4F,
    "p": 0x50, "q": 0x51, "r": 0x52, "s": 0x53, "t": 0x54,
    "u": 0x55, "v": 0x56, "w": 0x57, "x": 0x58, "y": 0x59, "z": 0x5A,
}

def get_vk_code(key):
    """Convert key name/string to virtual key code."""
    if isinstance(key, int):
        return key
    key_lower = key.lower()
    if key_lower in VK_CODES:
        return VK_CODES[key_lower]
    raise ValueError(f"Unknown key: {key}")

class KeyBdInput(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]

class HardwareInput(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_ushort),
    ]

class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput), ("mi", MouseInput), ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]

def press_key(vk):
    """Press a key using scan codes (works with DirectInput games)."""
    scan_code = MapVirtualKey(vk, MAPVK_VK_TO_VSC)
    extra = ctypes.c_ulong(0)
    ii = Input_I()
    # Use both VK and scan code with KEYEVENTF_SCANCODE flag
    ii.ki = KeyBdInput(0, scan_code, KEYEVENTF_SCANCODE, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii)
    result = SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    logger.debug(f"press_key: vk=0x{vk:02X}, scan=0x{scan_code:02X}, result={result}")

def release_key(vk):
    """Release a key using scan codes (works with DirectInput games)."""
    scan_code = MapVirtualKey(vk, MAPVK_VK_TO_VSC)
    extra = ctypes.c_ulong(0)
    ii = Input_I()
    # Use scan code with both SCANCODE and KEYUP flags
    ii.ki = KeyBdInput(0, scan_code, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii)
    result = SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    logger.debug(f"release_key: vk=0x{vk:02X}, scan=0x{scan_code:02X}, result={result}")

def post_key_to_window(hwnd, vk):
    """Send key directly to window using PostMessage (works even if window not focused)."""
    scan_code = MapVirtualKey(vk, MAPVK_VK_TO_VSC)
    lparam_down = (scan_code << 16) | 1
    lparam_up = (scan_code << 16) | 0xC0000001
    
    PostMessageW(hwnd, WM_KEYDOWN, vk, lparam_down)
    time.sleep(0.05)
    PostMessageW(hwnd, WM_KEYUP, vk, lparam_up)
    logger.debug(f"post_key_to_window: hwnd={hwnd}, vk=0x{vk:02X}, scan=0x{scan_code:02X}")

def tap_key(key, delay=0.1, use_postmessage=True):
    """
    Send a key press.
    
    Args:
        key: Key name or virtual key code
        delay: Delay between press and release
        use_postmessage: If True, use PostMessage (works in background). 
                         If False, use SendInput (requires focus).
    """
    vk = get_vk_code(key)
    logger.info(f"Tapping key '{key}' (vk=0x{vk:02X}, method={'PostMessage' if use_postmessage else 'SendInput'})")
    
    if use_postmessage and _target_hwnd:
        post_key_to_window(_target_hwnd, vk)
        time.sleep(delay)
    else:
        press_key(vk)
        time.sleep(delay)
        release_key(vk)
    
    logger.debug(f"Key '{key}' released")

def test_input(key="1"):
    """Test if input is working. Run this to debug input issues."""
    import ctypes
    
    # Check if running as admin
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    logger.info(f"Running as Administrator: {is_admin}")
    
    if not is_admin:
        logger.warning("NOT running as Administrator! This may cause input to fail.")
        logger.warning("Try: Right-click Python/script -> Run as administrator")
    
    vk = get_vk_code(key)
    scan = MapVirtualKey(vk, MAPVK_VK_TO_VSC)
    
    logger.info(f"Testing key '{key}': VK=0x{vk:02X}, ScanCode=0x{scan:02X}")
    logger.info(f"Target window hwnd: {_target_hwnd}")
    
    # Test SendInput
    logger.info("Testing SendInput method...")
    press_key(vk)
    time.sleep(0.1)
    release_key(vk)
    
    time.sleep(0.5)
    
    # Test PostMessage
    if _target_hwnd:
        logger.info("Testing PostMessage method...")
        post_key_to_window(_target_hwnd, vk)
    else:
        logger.warning("No target window set, skipping PostMessage test")
    
    logger.info("Input test complete. Check if the game received the key press.")
