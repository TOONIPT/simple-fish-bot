import json
import time
from gui import FishBotGUI
from window import get_window_rect, focus_window
from vision import Vision
from fisher import Fisher

FishBotGUI()

with open("config.json", "r") as f:
    cfg = json.load(f)

hwnd = int(cfg["window_hwnd"])

# 🔥 FOCO NA JANELA DO JOGO
focus_window(hwnd)
time.sleep(0.5)

rect = get_window_rect(hwnd)

vision = Vision(rect, cfg["vision"]["threshold"], cfg["vision"]["symbol"])
fisher = Fisher(cfg, vision)

print("Fish Bot ativo — Emphyr")

while True:
    fisher.fish_cycle()
