# api/logger.py
import logging

try:
    from pythonjsonlogger import jsonlogger  # type: ignore
    _HAS_JSONLOGGER = True
except Exception:
    jsonlogger = None
    _HAS_JSONLOGGER = False


def get_logger(name="fraud_api"):
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        if _HAS_JSONLOGGER:
            formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
        else:
            # fallback plain formatter
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger


# ➕ Fonction simple pour logger en JSON depuis main.py
logger = get_logger()


def log_json(data: dict):
    # If jsonlogger isn't available, this will still log a string representation
    logger.info(data)
