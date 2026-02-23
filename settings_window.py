from __future__ import annotations

try:
    from AppKit import (
        NSAlert,
        NSAlertFirstButtonReturn,
        NSAlertSecondButtonReturn,
        NSAlertStyleWarning,
        NSApplication,
        NSMakeRect,
        NSTextField,
        NSView,
    )
except Exception:  # pragma: no cover - AppKit is only available on macOS
    NSAlert = None
    NSAlertFirstButtonReturn = 1000
    NSAlertSecondButtonReturn = 1001
    NSAlertStyleWarning = None
    NSApplication = None
    NSMakeRect = None
    NSTextField = None
    NSView = None

from config import load_config, save_config


_DIALOG_SAVE_RESPONSE = int(NSAlertFirstButtonReturn)
_DIALOG_CANCEL_RESPONSE = int(NSAlertSecondButtonReturn)
_INTERVAL_ERROR = "Please enter an integer between 10 and 3600."


def _prompt_settings(default_token: str, default_interval: int) -> tuple[str, int] | None:
    token_value = default_token
    interval_value = str(default_interval)

    while True:
        response, token_value, interval_value = _show_settings_dialog(token_value, interval_value)

        if response != _DIALOG_SAVE_RESPONSE:
            return None

        token_key = token_value.strip()
        interval_text = interval_value.strip()

        try:
            interval = int(interval_text)
        except ValueError:
            _show_error_alert(_INTERVAL_ERROR)
            continue

        if not (10 <= interval <= 3600):
            _show_error_alert(_INTERVAL_ERROR)
            continue

        return token_key, interval


def _show_settings_dialog(default_token: str, default_interval: str) -> tuple[int, str, str]:
    if NSAlert is None or NSView is None or NSTextField is None or NSMakeRect is None:
        raise RuntimeError("macOS AppKit is required to open settings")

    if NSApplication is not None:
        NSApplication.sharedApplication().activateIgnoringOtherApps_(True)

    alert = NSAlert.alloc().init()
    alert.setMessageText_("Token Icon Settings")
    alert.setInformativeText_("Set token key and refresh interval.")
    alert.addButtonWithTitle_("Save")
    alert.addButtonWithTitle_("Cancel")

    container = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, 420, 90))

    token_label = _make_label("Token Key", NSMakeRect(0, 68, 140, 16))
    token_field = NSTextField.alloc().initWithFrame_(NSMakeRect(0, 44, 420, 22))
    token_field.setStringValue_(default_token)

    interval_label = _make_label("Refresh interval (10-3600)", NSMakeRect(0, 22, 220, 16))
    interval_field = NSTextField.alloc().initWithFrame_(NSMakeRect(0, 0, 140, 22))
    interval_field.setStringValue_(default_interval)

    container.addSubview_(token_label)
    container.addSubview_(token_field)
    container.addSubview_(interval_label)
    container.addSubview_(interval_field)

    alert.setAccessoryView_(container)
    response = int(alert.runModal())
    return response, str(token_field.stringValue()), str(interval_field.stringValue())


def _make_label(text: str, frame):
    label = NSTextField.alloc().initWithFrame_(frame)
    label.setStringValue_(text)
    label.setBezeled_(False)
    label.setDrawsBackground_(False)
    label.setEditable_(False)
    label.setSelectable_(False)
    return label


def _show_error_alert(message: str) -> None:
    if NSAlert is None:
        raise RuntimeError(message)

    if NSApplication is not None:
        NSApplication.sharedApplication().activateIgnoringOtherApps_(True)

    alert = NSAlert.alloc().init()
    alert.setMessageText_("Invalid interval")
    alert.setInformativeText_(message)
    if NSAlertStyleWarning is not None:
        alert.setAlertStyle_(NSAlertStyleWarning)
    alert.addButtonWithTitle_("OK")
    alert.runModal()


def open_settings(on_save_callback=None):
    config = load_config()
    result = _prompt_settings(config["token_key"], config["refresh_interval"])
    if result is None:
        return

    token_key, interval = result
    save_config({"token_key": token_key, "refresh_interval": interval})

    if on_save_callback:
        on_save_callback()
