import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "board": {
        "x": 0,
        "y": 0,
        "w": 0,
        "h": 0
    },
    "depth": 5,
    "move_delay": 0.05,
    "use_adb": True,
    "adb_serial": ""
}


def load():
    if not os.path.exists(CONFIG_FILE):
        save(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4)