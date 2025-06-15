# logging_config.py
import logging
from logging.handlers import RotatingFileHandler
import os

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

def create_logger(name: str, filename: str, level=logging.INFO, to_stdout=False):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s | request #%(request_id)s",
        datefmt="%d-%m-%Y %H:%M:%S.%f"
    )

    file_handler = RotatingFileHandler(os.path.join(LOGS_DIR, filename), maxBytes=5*1024*1024, backupCount=3)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if to_stdout:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger
