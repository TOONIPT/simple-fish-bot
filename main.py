import json
import time
import logging
from gui import FishBotGUI
from window import get_window_rect, focus_window
from vision import Vision
from fisher import Fisher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("fishbot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("FishBot")

logger.info("Starting Fish Bot...")

FishBotGUI()

logger.info("Loading configuration from config.json")
with open("config.json", "r") as f:
    cfg = json.load(f)
logger.info(f"Configuration loaded: window_hwnd={cfg['window_hwnd']}")

hwnd = int(cfg["window_hwnd"])

logger.info(f"Focusing game window (hwnd={hwnd})")
focus_window(hwnd)
time.sleep(0.5)

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
