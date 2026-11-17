# -------- Imports --------
import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from dotenv import load_dotenv
import os
from .definitions import ConfigError

# -------- Variables --------
LOG_FILE = Path(__file__).resolve().parent.parent / "logs" / f"bot-{datetime.now():%Y-%m-%d_%H-%M-%S-%f}.log"
LOG_FORMAT = "%(asctime)s | [%(levelname)s] | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# -- Validate the amount of logs to keep
load_dotenv()
keep_log_ammount = os.getenv("LOG_AMMOUNT", "").strip()

if keep_log_ammount:
    try:
        keep_log_ammount = int(keep_log_ammount)
    except ValueError:
        raise ConfigError(
            "[Logging] LOG_AMMOUNT must be a valid number."
        )

    if not 0 <= keep_log_ammount:
        raise ConfigError(
            "[Logging] LOG_AMMOUNT must be greater than 0."
        )

# -------- Cleanup Log Files --------
def cleanup_log_files(log_dir: Path, current_log: Path) -> None:
    # -- Find all log files
    log_files = [path for path in log_dir.glob("bot-*.log*") if path.is_file()]
    log_files.sort(key=lambda path: path.stat().st_mtime, reverse=True)

    kept_files = {current_log}
    for path in log_files:
        if len(kept_files) >= keep_log_ammount:
            break
        kept_files.add(path)

    # -- Delete old log files
    for path in log_files:
        if path not in kept_files:
            path.unlink()
class LogFileHandler(RotatingFileHandler):
    def doRollover(self) -> None:
        super().doRollover()
        cleanup_log_files(Path(self.baseFilename).parent, Path(self.baseFilename))

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
    if type(keep_log_ammount) == int:
        if keep_log_ammount > 0:
            if not any(isinstance(handler, RotatingFileHandler) and Path(handler.baseFilename) == resolved_log_file for handler in logger.handlers):
                resolved_log_file.parent.mkdir(parents=True, exist_ok=True)
                file_handler = LogFileHandler(resolved_log_file, maxBytes=5 * 1024 * 1024, backupCount=4, encoding="utf-8")
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)

        cleanup_log_files(resolved_log_file.parent, resolved_log_file)
    return logger

logger = setup_logger()
