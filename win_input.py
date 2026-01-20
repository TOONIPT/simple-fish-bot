import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

PUL = ctypes.POINTER(ctypes.c_ulong)

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

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]

def press_key(vk):
    extra = ctypes.c_ulong(0)
    ii = Input_I()
    ii.ki = KeyBdInput(vk, 0, 0, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def release_key(vk):
    extra = ctypes.c_ulong(0)
    ii = Input_I()
    ii.ki = KeyBdInput(vk, 0, 2, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def tap_key(key, delay=0.1):
    vk = get_vk_code(key)
    press_key(vk)
    time.sleep(delay)
    release_key(vk)
