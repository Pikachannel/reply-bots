# -------- Imports --------
import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

# -------- Variables --------
LOG_FILE = Path(__file__).resolve().parent.parent / "logs" / f"bot-{datetime.now():%Y-%m-%d_%H-%M-%S-%f}.log"
LOG_FORMAT = "%(asctime)s | [%(levelname)s] | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# -------- Setup Logger --------
def setup_logger(level: str = "") -> logging.Logger:
    logger = logging.getLogger("reply-bots")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.propagate = False

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    # -- Console handler
    if not any(isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler) for handler in logger.handlers):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # -- File handler
    resolved_log_file = Path(LOG_FILE).resolve()
    if not any(isinstance(handler, RotatingFileHandler) and Path(handler.baseFilename) == resolved_log_file for handler in logger.handlers):
        resolved_log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(resolved_log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

logger = setup_logger()
