import time
from win_input import tap_key


class Fisher:
    def __init__(self, cfg, vision):
        self.cfg = cfg
        self.vision = vision

    def equip_bait(self):
        print("Equipar isco")
        pyautogui.press(self.cfg["keys"]["equip_bait"])
        time.sleep(self.cfg["timing"]["after_bait"])

    def cast(self):
        print("➡️ Lançar cana")
        pyautogui.press(self.cfg["keys"]["fish"])

    def fish_cycle(self):
        self.equip_bait()
        self.cast()

        print("À espera da mordida...")
        start = time.time()

        while time.time() - start < self.cfg["timing"]["wait_bite_max"]:
            if self.vision.detect_bite():
                print("🐟 Mordida detetada! Recolher cana")
                pyautogui.press(self.cfg["keys"]["fish"])
                time.sleep(1.2)
                return True

            time.sleep(self.cfg["timing"]["scan_interval"])

        print("Timeout, sem peixe")
        return False
