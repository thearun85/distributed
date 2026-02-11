"""
SWIM - Distributed systems protocol - standard message formats
"""
import json
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
def create_ping(sender: str, host:str, port: int, sequence: int):
    return json.dumps({
        "type": "PING",
        "sender": sender,
        "host": host,
        "port": port,
        "sequence": sequence,
    })

def create_ack(sender: str, sequence: int, on_behalf_of: str = None:
    return json.dumps({
        "type": "ACK",
        "sender": sender,
        "sequence": sequence,
        "on_behalf_of": on_behalf_of, # in case of PING_REQ
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

def create_ping_req(sender: str, host: str, port: int, sequence: int,
                target_node: str, target_host: str, target_port: int):
    return json.dumps({
        "type": "PING_REQ",
        "sender": sender,
        "host": host,
        "port": port,
        "sequence": sequence,
        "target_node": target_node,
        "target_host": target_host,
        "target_port": target_port,
    })
