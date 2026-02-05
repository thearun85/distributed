"""
SWIM - Distributed protocol - helper functions
"""
import socket
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import json
import random

from .messages import create_ping, parse_message

def send_ping(target_host: str, target_port: int):
    """Send a message to a node """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect((target_host, target_port))
            
    try:
        msg = create_ping("test-node", random.randint(1, 1000))
        sock.send(msg.encode('utf-8'))
        data = sock.recv(1024)
        if data:
            message_str = data.decode('utf-8')
            message = parse_message(message_str)
            if message and message['type'] == 'ACK':
                logger.info(f"[Helper function] Acknowledgement received from {message['sender']}")
        else:
            logger.info(f"[Helper function] Empty data")
    except Exception as e:
        logger.error(f"[Helper function] Error while sending a message: {e}")
    finally:
        logger.info(f"[Helper function] closed the connection")
        sock.close()
    
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: python helper.py <host> <port>")
        sys.exit(1)
        
    send_ping(sys.argv[1], int(sys.argv[2]))

    parse_message(json.dumps({"test": "test"}))
