import logging
from datetime import datetime
from pathlib import Path
from dynalog.config import config
import pytz


class DefaultFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt=fmt, datefmt=datefmt)

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, pytz.timezone(config.get("tz")))
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat()

    def format(self, record):
        # Ensure full file path is included
        record.full_path = record.pathname  # full absolute path of the source file
        return super().format(record)


def get_logger(init: bool = True) -> logging.Logger:
    name = config.get("logs__name", "NO_NAME")
    if not init:
        return logging.getLogger(name)

    logger = logging.getLogger(name)
    log_file_path = config.get("logs__file")
    log_dir = Path(log_file_path).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    logger.setLevel(getattr(logging, config.get("logs__level", "INFO").upper()))

    # Include log_file_path in the format string
    fmt = "[%(asctime)s] %(levelname)s [%(full_path)s]: %(message)s"
    formatter = DefaultFormatter(fmt=fmt)

    # File handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logger.level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if config.get("logs__enable_stream", False):
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logger.level)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger
