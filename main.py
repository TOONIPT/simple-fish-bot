import json
import time
import logging
import sys
import os
import threading
import keyboard
from gui import FishBotGUI
from window import get_window_rect, focus_window
from vision import Vision
from fisher import Fisher
from win_input import set_target_window, test_input

# Global flag to control the bot
bot_running = True
bot_paused = False

def stop_bot():
    """Stop the bot completely."""
    global bot_running
    bot_running = False
    logger.info("STOP signal received! Shutting down...")

def toggle_pause():
    """Pause/resume the bot."""
    global bot_paused
    bot_paused = not bot_paused
    if bot_paused:
        logger.info("BOT PAUSED - Press F10 to resume")
    else:
        logger.info("BOT RESUMED")

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# Configure logging
log_path = get_resource_path("fishbot.log")
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for troubleshooting
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("FishBot")

logger.info("Starting Fish Bot...")
logger.info(f"Base path: {get_resource_path('.')}")

# Check if running as admin
import ctypes
is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
if is_admin:
    logger.info("Running as Administrator - OK")
else:
    logger.warning("=" * 50)
    logger.warning("NOT RUNNING AS ADMINISTRATOR!")
    logger.warning("Input may not work. Please run as Administrator.")
    logger.warning("=" * 50)

FishBotGUI()

config_path = get_resource_path("config.json")
logger.info(f"Loading configuration from {config_path}")
with open(config_path, "r") as f:
    cfg = json.load(f)
logger.info(f"Configuration loaded: window_hwnd={cfg['window_hwnd']}")

hwnd = int(cfg["window_hwnd"])

# Set target window for PostMessage input method
set_target_window(hwnd)

logger.info(f"Focusing game window (hwnd={hwnd})")
focus_window(hwnd)
time.sleep(0.5)

# Test mode - run with --test argument
if "--test" in sys.argv:
    logger.info("=== INPUT TEST MODE ===")
    logger.info("Make sure the game window is focused!")
    time.sleep(2)
    test_input(cfg["keys"]["equip_bait"])
    sys.exit(0)

rect = get_window_rect(hwnd)
logger.info(f"Window rect: {rect}")

logger.info(f"Initializing Vision with threshold={cfg['vision']['threshold']}")
vision = Vision(rect, cfg["vision"]["threshold"], cfg["vision"]["symbol"])

logger.info("Initializing Fisher")
fisher = Fisher(cfg, vision)

# Register hotkeys
keyboard.add_hotkey('F12', stop_bot)
keyboard.add_hotkey('F10', toggle_pause)

logger.info("=" * 50)
logger.info("Fish Bot ativo - Emphyr")
logger.info("HOTKEYS:")
logger.info("  F10 = Pause/Resume")
logger.info("  F12 = Stop bot")
logger.info("=" * 50)
logger.info("Starting fishing loop...")

cycle_count = 0
while bot_running:
    if bot_paused:
        time.sleep(0.1)
        continue
    
    cycle_count += 1
    logger.info(f"=== Starting fish cycle #{cycle_count} ===")
    fisher.fish_cycle()

logger.info(f"Bot stopped after {cycle_count} cycles. Goodbye!")
keyboard.unhook_all()
