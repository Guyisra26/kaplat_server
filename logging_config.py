# logging_config.py
import logging
from logging.handlers import RotatingFileHandler
import os

LOGS_DIR = "logs"
# os.makedirs(LOGS_DIR, exist_ok=True)
class EnsureRequestIdFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, "request_id"):
            record.request_id = "-"
        return True

def create_logger(name: str, filename: str, level=logging.INFO, to_stdout=False):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s.%(msecs)03d %(levelname)s: %(message)s | request #%(request_id)s",
        datefmt="%d-%m-%Y %H:%M:%S"
    )
    logger.addFilter(EnsureRequestIdFilter())

    # file_handler = RotatingFileHandler(os.path.join(LOGS_DIR, filename), maxBytes=5*1024*1024, backupCount=3)
    # file_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)
    if to_stdout:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    try:
        os.makedirs(LOGS_DIR, exist_ok=True)
        fh = RotatingFileHandler(os.path.join(LOGS_DIR, filename), maxBytes=5 * 1024 * 1024, backupCount=3)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    except Exception:
        logger.addHandler(logging.NullHandler())

    return logger
