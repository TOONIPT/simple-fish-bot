import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

PUL = ctypes.POINTER(ctypes.c_ulong)

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

def tap_key(vk, delay=0.1):
    press_key(vk)
    time.sleep(delay)
    release_key(vk)
