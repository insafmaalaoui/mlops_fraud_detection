import logging
import json

logger = logging.getLogger("fraud_api")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_json(event: dict):
    logger.info(json.dumps(event))
