import tkinter as tk
from tkinter import ttk, messagebox
import json
from window import list_windows

CONFIG_FILE = "config.json"

class FishBotGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Metin2 Fish Bot – Emphyr")
        self.root.resizable(False, False)

        self.windows = list_windows()
        self.window_map = {
            f"{title} | HWND:{hwnd} | PID:{pid}": hwnd
            for hwnd, title, pid in self.windows
        }

        self.create_widgets()
        self.load_config()

        self.root.mainloop()

    def create_widgets(self):
        padding = {"padx": 10, "pady": 6}

        ttk.Label(self.root, text="Janela do Jogo").grid(row=0, column=0, **padding)
        self.window_combo = ttk.Combobox(
            self.root, values=list(self.window_map.keys()), width=55, state="readonly"
        )
        self.window_combo.grid(row=0, column=1, **padding)

        ttk.Label(self.root, text="Tecla do Isco").grid(row=1, column=0, **padding)
        self.bait_key = ttk.Entry(self.root)
        self.bait_key.grid(row=1, column=1, **padding)

        ttk.Label(self.root, text="Tecla Pescar").grid(row=2, column=0, **padding)
        self.fish_key = ttk.Entry(self.root)
        self.fish_key.grid(row=2, column=1, **padding)

        ttk.Label(self.root, text="Sensibilidade (0.6–0.95)").grid(row=3, column=0, **padding)
        self.threshold = ttk.Entry(self.root)
        self.threshold.grid(row=3, column=1, **padding)

        ttk.Button(self.root, text="Salvar", command=self.save).grid(row=4, column=0, **padding)
        ttk.Button(self.root, text="Iniciar Bot", command=self.start).grid(row=4, column=1, **padding)

    def load_config(self):
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)

        for label, hwnd in self.window_map.items():
            if str(hwnd) == str(cfg.get("window_hwnd")):
                self.window_combo.set(label)

        self.bait_key.insert(0, cfg["keys"]["equip_bait"])
        self.fish_key.insert(0, cfg["keys"]["fish"])
        self.threshold.insert(0, cfg["vision"]["threshold"])

    def save(self):
        if not self.window_combo.get():
            messagebox.showerror("Erro", "Seleciona a janela do Metin2")
            return

        selected_label = self.window_combo.get()
        hwnd = self.window_map[selected_label]

        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)

        cfg["window_hwnd"] = hwnd
        cfg["keys"]["equip_bait"] = self.bait_key.get()
        cfg["keys"]["fish"] = self.fish_key.get()
        cfg["vision"]["threshold"] = float(self.threshold.get())

        with open(CONFIG_FILE, "w") as f:
            json.dump(cfg, f, indent=2)

        messagebox.showinfo("OK", "Configuração guardada")

    def start(self):
        self.save()
        self.root.destroy()
