import time
import logging
from win_input import tap_key

logger = logging.getLogger("FishBot.Fisher")


class Fisher:
    def __init__(self, cfg, vision):
        self.cfg = cfg
        self.vision = vision
        logger.debug("Fisher initialized")

    def equip_bait(self):
        logger.info(f"Equipping bait (key={self.cfg['keys']['equip_bait']})")
        tap_key(self.cfg["keys"]["equip_bait"])
        time.sleep(self.cfg["timing"]["after_bait"])
        logger.debug(f"Waited {self.cfg['timing']['after_bait']}s after bait")

    def cast(self):
        logger.info(f"Casting rod (key={self.cfg['keys']['fish']})")
        tap_key(self.cfg["keys"]["fish"])

    def fish_cycle(self):
        self.equip_bait()
        self.cast()

        logger.info(f"Waiting for bite (max {self.cfg['timing']['wait_bite_max']}s)...")
        start = time.time()

        while time.time() - start < self.cfg["timing"]["wait_bite_max"]:
            if self.vision.detect_bite():
                elapsed = time.time() - start
                logger.info(f"Bite detected after {elapsed:.2f}s! Reeling in...")
                tap_key(self.cfg["keys"]["fish"])
                time.sleep(1.2)
                logger.info("Fish caught successfully!")
                return True

            time.sleep(self.cfg["timing"]["scan_interval"])

        elapsed = time.time() - start
        logger.warning(f"Timeout after {elapsed:.2f}s - no fish caught")
        return False
