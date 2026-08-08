import logging
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.getenv('AWS_ACCESS_ID')
SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_DEFAULT_REGION', 'eu-central-1')


def set_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate log entries if set_logger is called repeatedly
    if not logger.handlers:
        filehandler = logging.FileHandler("ingest.log", mode="a", encoding="utf-8")
        formatter = logging.Formatter(
            "{asctime} - {levelname} - {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M"
        )
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)

    return logger

