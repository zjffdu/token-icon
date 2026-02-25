from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from config import CONFIG_DIR

LOG_DIR = CONFIG_DIR / "logs"
LOG_FILE = LOG_DIR / "token-icon.log"
LOGGER_NAME = "token_icon"


def setup_logging() -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False

    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=512 * 1024,
            backupCount=3,
            encoding="utf-8",
        )
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
        logger.addHandler(handler)
    except OSError:
        logger.addHandler(logging.NullHandler())

    return logger
