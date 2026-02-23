import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "token-icon"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULTS = {
    "token_key": "",
    "refresh_interval": 60,
}


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        return DEFAULTS.copy()
    try:
        with open(CONFIG_FILE) as f:
            data = json.load(f)
        return {**DEFAULTS, **data}
    except (json.JSONDecodeError, OSError):
        return DEFAULTS.copy()


def save_config(config: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
