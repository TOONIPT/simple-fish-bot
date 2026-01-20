import json
import time
import logging
import sys
from gui import FishBotGUI
from window import get_window_rect, focus_window
from vision import Vision
from fisher import Fisher
from win_input import set_target_window, test_input

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for troubleshooting
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("fishbot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("FishBot")

logger.info("Starting Fish Bot...")

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

logger.info("Loading configuration from config.json")
with open("config.json", "r") as f:
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

logger.info("Fish Bot ativo - Emphyr")
logger.info("Starting fishing loop...")

cycle_count = 0
while True:
    cycle_count += 1
    logger.info(f"=== Starting fish cycle #{cycle_count} ===")
    fisher.fish_cycle()
