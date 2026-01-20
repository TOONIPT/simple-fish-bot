import cv2
import numpy as np
from mss import mss

class Vision:
    def __init__(self, window_rect, threshold, symbol_path):
        self.sct = mss()
        self.monitor = window_rect
        self.threshold = threshold
        self.symbol = cv2.imread(symbol_path, 0)

        if self.symbol is None:
            raise RuntimeError("Não foi possível carregar bite_symbol.png")

        self.sym_h, self.sym_w = self.symbol.shape[:2]

    def detect_bite(self):
        frame = np.array(self.sct.grab(self.monitor))

        # ⚠️ Proteção contra captura inválida
        if frame.size == 0:
            return False

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape[:2]

        # ⚠️ PROTEÇÃO CRÍTICA (evita o crash)
        if h < self.sym_h or w < self.sym_w:
            return False

        res = cv2.matchTemplate(gray, self.symbol, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)

        return max_val >= self.threshold
