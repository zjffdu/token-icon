import json
import subprocess
import sys

from config import load_config, save_config


_SETTINGS_DIALOG_SCRIPT = r"""
import json
import sys
import tkinter as tk
from tkinter import messagebox

default_token = sys.argv[1]
default_interval = sys.argv[2]

state = {"code": 2, "payload": None}

root = tk.Tk()
root.title("Token Icon Settings")
root.resizable(False, False)
try:
    root.attributes("-topmost", True)
except Exception:
    pass

frame = tk.Frame(root, padx=12, pady=12)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="Token Key").grid(row=0, column=0, columnspan=2, sticky="w")
token_entry = tk.Entry(frame, width=48)
token_entry.grid(row=1, column=0, columnspan=2, sticky="we", pady=(2, 10))
token_entry.insert(0, default_token)

tk.Label(frame, text="Refresh interval (10-3600)").grid(row=2, column=0, columnspan=2, sticky="w")
interval_entry = tk.Entry(frame, width=16)
interval_entry.grid(row=3, column=0, sticky="w", pady=(2, 0))
interval_entry.insert(0, default_interval)

buttons = tk.Frame(frame)
buttons.grid(row=4, column=0, columnspan=2, sticky="e", pady=(12, 0))

def on_cancel():
    state["code"] = 2
    root.quit()

def on_save():
    token_key = token_entry.get().strip()
    interval_text = interval_entry.get().strip()
    try:
        interval = int(interval_text)
    except ValueError:
        messagebox.showerror(
            "Invalid interval",
            "Please enter an integer between 10 and 3600.",
            parent=root,
        )
        return

    if not (10 <= interval <= 3600):
        messagebox.showerror(
            "Invalid interval",
            "Please enter an integer between 10 and 3600.",
            parent=root,
        )
        return

    state["payload"] = {"token_key": token_key, "refresh_interval": interval}
    state["code"] = 0
    root.quit()

cancel_btn = tk.Button(buttons, text="Cancel", width=9, command=on_cancel)
cancel_btn.pack(side="right")
save_btn = tk.Button(buttons, text="Save", width=9, command=on_save)
save_btn.pack(side="right", padx=(0, 8))

root.bind("<Return>", lambda _evt: on_save())
root.bind("<Escape>", lambda _evt: on_cancel())
root.protocol("WM_DELETE_WINDOW", on_cancel)
token_entry.focus_set()
root.mainloop()
root.destroy()

if state["code"] == 0:
    print(json.dumps(state["payload"]))
sys.exit(state["code"])
"""


def _prompt_settings(default_token: str, default_interval: int) -> tuple[str, int] | None:
    result = subprocess.run(
        [sys.executable, "-c", _SETTINGS_DIALOG_SCRIPT, default_token, str(default_interval)],
        capture_output=True,
        text=True,
    )

    if result.returncode == 2:
        return None
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Failed to open settings dialog")

    try:
        payload = json.loads(result.stdout.strip())
        token_key = str(payload["token_key"])
        interval = int(payload["refresh_interval"])
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        raise RuntimeError("Invalid settings dialog result") from exc

    return token_key, interval


def open_settings(on_save_callback=None):
    config = load_config()
    result = _prompt_settings(config["token_key"], config["refresh_interval"])
    if result is None:
        return

    token_key, interval = result
    save_config({"token_key": token_key, "refresh_interval": interval})

    if on_save_callback:
        on_save_callback()
