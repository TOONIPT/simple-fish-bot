import cv2
import numpy as np
import logging
import os
import sys
from mss import mss

logger = logging.getLogger("FishBot.Vision")

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


class Vision:
    def __init__(self, window_rect, threshold, symbol_path):
        logger.info(f"Initializing Vision system")
        logger.debug(f"Window rect: {window_rect}")
        logger.debug(f"Threshold: {threshold}")
        logger.debug(f"Symbol path (relative): {symbol_path}")
        
        # Resolve to absolute path
        abs_symbol_path = get_resource_path(symbol_path)
        logger.debug(f"Symbol path (absolute): {abs_symbol_path}")
        
        self.sct = mss()
        self.monitor = window_rect
        self.threshold = threshold
        self.symbol = cv2.imread(abs_symbol_path, 0)

        if self.symbol is None:
            logger.error(f"Failed to load symbol image: {abs_symbol_path}")
            logger.error(f"File exists: {os.path.exists(abs_symbol_path)}")
            raise RuntimeError(f"Nao foi possivel carregar {abs_symbol_path}")

        self.sym_h, self.sym_w = self.symbol.shape[:2]
        logger.info(f"Symbol loaded: {self.sym_w}x{self.sym_h} pixels")

    def detect_bite(self):
        frame = np.array(self.sct.grab(self.monitor))

        # Protection against invalid capture
        if frame.size == 0:
            logger.warning("Invalid frame capture (empty frame)")
            return False

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape[:2]

        # Critical protection (prevents crash)
        if h < self.sym_h or w < self.sym_w:
            logger.warning(f"Frame too small: {w}x{h} < symbol {self.sym_w}x{self.sym_h}")
            return False

        res = cv2.matchTemplate(gray, self.symbol, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)

        logger.debug(f"Template match: {max_val:.3f} (threshold: {self.threshold})")
        
        if max_val >= self.threshold:
            logger.debug(f"Bite detected! Match value: {max_val:.3f}")
            return True
        return False
