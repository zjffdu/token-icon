import threading
import rumps
from api import fetch_token_stats
from app_logging import LOG_FILE, setup_logging
from config import load_config
from settings_window import open_settings as _open_settings
from title_format import format_menu_title


class TokenIconApp(rumps.App):
    def __init__(self):
        super().__init__(format_menu_title("—"), quit_button=None)
        self._logger = setup_logging()
        self._item_remain = rumps.MenuItem("Remaining: —")
        self._item_used = rumps.MenuItem("Used today: —")
        self._item_added = rumps.MenuItem("Added today: —")
        self._item_status = rumps.MenuItem("Status: —")
        self.menu = [
            self._item_remain,
            self._item_used,
            self._item_added,
            self._item_status,
            None,
            rumps.MenuItem("Refresh Now", callback=self.refresh_now),
            rumps.MenuItem("Settings...", callback=self.open_settings),
            None,
            rumps.MenuItem("Quit", callback=rumps.quit_application),
        ]
        self._timer = rumps.Timer(self._on_tick, self._get_interval())
        self._timer.start()
        self._logger.info("app started refresh_interval=%s log_file=%s", self._get_interval(), LOG_FILE)
        self._fetch_in_background()

    def _get_interval(self):
        return load_config()["refresh_interval"]

    def _on_tick(self, _):
        self._fetch_in_background()

    def _fetch_in_background(self):
        t = threading.Thread(target=self._fetch, daemon=True)
        t.start()

    def _fetch(self):
        config = load_config()
        try:
            data = fetch_token_stats(config["token_key"])
            self._update_menu(data)
        except ValueError:
            self.title = format_menu_title("—")
            self._item_status.title = "Status: token not configured"
            self._logger.info("fetch skipped: token_key not configured")
        except Exception as e:
            self.title = format_menu_title("!")
            self._item_status.title = f"Error: {e}"
            self._logger.exception("fetch failed")

    def _update_menu(self, data):
        token_info = data.get("data", {}).get("token_info", {})
        today = data.get("data", {}).get("today_stats", {})
        remain = token_info.get("remain_quota_display", "—")
        used = today.get("used_quota", "—")
        added = today.get("added_quota", "—")
        status = token_info.get("status", {}).get("text", "—")

        self.title = format_menu_title(remain)
        self._item_remain.title = f"Remaining: {remain}"
        self._item_used.title = f"Used today: {used}"
        self._item_added.title = f"Added today: {added}"
        self._item_status.title = f"Status: {status}"

    def refresh_now(self, _):
        self._logger.info("manual refresh requested")
        self._fetch_in_background()

    def open_settings(self, _):
        self._logger.info("settings opened")

        def on_save():
            self._timer.stop()
            self._timer = rumps.Timer(self._on_tick, self._get_interval())
            self._timer.start()
            self._fetch_in_background()
            self._logger.info("settings saved refresh_interval=%s", self._get_interval())

        try:
            _open_settings(on_save_callback=on_save)
        except Exception as e:
            self._item_status.title = f"Status: Settings error: {e}"
            self._logger.exception("settings dialog failed")
            rumps.alert("Settings error", str(e))


if __name__ == "__main__":
    TokenIconApp().run()
