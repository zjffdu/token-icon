import importlib
import logging
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


class TestAppLogging(unittest.TestCase):
    def setUp(self):
        self._logger = logging.getLogger("token_icon")
        self._old_handlers = list(self._logger.handlers)
        self._old_level = self._logger.level
        self._old_propagate = self._logger.propagate
        for handler in list(self._logger.handlers):
            self._logger.removeHandler(handler)
            handler.close()

    def tearDown(self):
        for handler in list(self._logger.handlers):
            self._logger.removeHandler(handler)
            handler.close()

        self._logger.setLevel(self._old_level)
        self._logger.propagate = self._old_propagate
        for handler in self._old_handlers:
            self._logger.addHandler(handler)

    def test_setup_logging_creates_log_file_and_writes_messages(self):
        with tempfile.TemporaryDirectory() as tmp:
            log_dir = Path(tmp) / "logs"
            log_file = log_dir / "token-icon.log"

            app_logging = importlib.import_module("app_logging")
            with patch.object(app_logging, "LOG_DIR", log_dir), patch.object(app_logging, "LOG_FILE", log_file):
                logger = app_logging.setup_logging()
                logger.error("test-log-message")
                for handler in logger.handlers:
                    handler.flush()

            self.assertTrue(log_file.exists())
            content = log_file.read_text(encoding="utf-8")
            self.assertIn("test-log-message", content)

    def test_setup_logging_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            log_dir = Path(tmp) / "logs"
            log_file = log_dir / "token-icon.log"

            app_logging = importlib.import_module("app_logging")
            with patch.object(app_logging, "LOG_DIR", log_dir), patch.object(app_logging, "LOG_FILE", log_file):
                logger_one = app_logging.setup_logging()
                logger_two = app_logging.setup_logging()

            self.assertIs(logger_one, logger_two)
            self.assertEqual(len(logger_one.handlers), 1)


if __name__ == "__main__":
    unittest.main()
