"""
SWIM - Distributed systems protocol - standard message formats
"""
import json
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
def create_ping(sender: str, sequence: int):
    return json.dumps({
        "type": "PING",
        "sender": sender,
        "sequence": sequence,
    })

def create_ack(sender: str, sequence: int):
    return json.dumps({
        "type": "ACK",
        "sender": sender,
        "sequence": sequence,
    })

def parse_message(message: str):
    try:
        return json.loads(message)
    except json.JSONDecodeError as e:
        logging.error(f"[parse_message] JSON DecodeError: {e}")
        return None
    except Exception as e:
        logging.error(f"[parse_message] Exception: {e}")
        return None
