import subprocess
import unittest
from unittest.mock import patch

import settings_window


class TestSettingsWindow(unittest.TestCase):
    def test_prompt_settings_parses_single_dialog_result(self):
        completed = subprocess.CompletedProcess(
            args=["python"],
            returncode=0,
            stdout='{"token_key": "abc-key", "refresh_interval": 120}\n',
            stderr="",
        )
        with patch("settings_window.subprocess.run", return_value=completed):
            result = settings_window._prompt_settings("old-token", 60)

        self.assertEqual(result, ("abc-key", 120))

    def test_prompt_settings_returns_none_when_canceled(self):
        completed = subprocess.CompletedProcess(
            args=["python"],
            returncode=2,
            stdout="",
            stderr="",
        )
        with patch("settings_window.subprocess.run", return_value=completed):
            result = settings_window._prompt_settings("old-token", 60)

        self.assertIsNone(result)

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
