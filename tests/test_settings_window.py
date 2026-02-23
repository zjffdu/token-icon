import unittest
from unittest.mock import patch

import settings_window


class TestSettingsWindow(unittest.TestCase):
    def test_prompt_settings_returns_values_when_saved(self):
        with patch(
            "settings_window._show_settings_dialog",
            return_value=(settings_window._DIALOG_SAVE_RESPONSE, " abc-key ", " 120 "),
        ):
            result = settings_window._prompt_settings("old-token", 60)

        self.assertEqual(result, ("abc-key", 120))

    def test_prompt_settings_returns_none_when_canceled(self):
        with patch(
            "settings_window._show_settings_dialog",
            return_value=(settings_window._DIALOG_CANCEL_RESPONSE, "", "60"),
        ):
            result = settings_window._prompt_settings("old-token", 60)

        self.assertIsNone(result)

    def test_prompt_settings_retries_when_interval_not_integer(self):
        with patch(
            "settings_window._show_settings_dialog",
            side_effect=[
                (settings_window._DIALOG_SAVE_RESPONSE, "abc-key", "oops"),
                (settings_window._DIALOG_SAVE_RESPONSE, "abc-key", "300"),
            ],
        ) as mock_dialog, patch("settings_window._show_error_alert") as mock_error:
            result = settings_window._prompt_settings("old-token", 60)

        self.assertEqual(result, ("abc-key", 300))
        self.assertEqual(mock_dialog.call_count, 2)
        mock_error.assert_called_once()

    def test_prompt_settings_retries_when_interval_out_of_range(self):
        with patch(
            "settings_window._show_settings_dialog",
            side_effect=[
                (settings_window._DIALOG_SAVE_RESPONSE, "abc-key", "5"),
                (settings_window._DIALOG_SAVE_RESPONSE, "abc-key", "300"),
            ],
        ) as mock_dialog, patch("settings_window._show_error_alert") as mock_error:
            result = settings_window._prompt_settings("old-token", 60)

        self.assertEqual(result, ("abc-key", 300))
        self.assertEqual(mock_dialog.call_count, 2)
        mock_error.assert_called_once()

    def test_open_settings_saves_config_from_single_dialog(self):
        callback_calls = {"count": 0}

        with patch("settings_window.load_config", return_value={"token_key": "old", "refresh_interval": 60}), \
             patch("settings_window._prompt_settings", return_value=("new-token", 300)), \
             patch("settings_window.save_config") as mock_save:
            settings_window.open_settings(lambda: callback_calls.__setitem__("count", callback_calls["count"] + 1))

        mock_save.assert_called_once_with({"token_key": "new-token", "refresh_interval": 300})
        self.assertEqual(callback_calls["count"], 1)

    def test_open_settings_does_not_save_when_canceled(self):
        with patch("settings_window.load_config", return_value={"token_key": "old", "refresh_interval": 60}), \
             patch("settings_window._prompt_settings", return_value=None), \
             patch("settings_window.save_config") as mock_save:
            settings_window.open_settings()

        mock_save.assert_not_called()


if __name__ == "__main__":
    unittest.main()
