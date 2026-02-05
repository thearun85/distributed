"""
SWIM - Distributed protocol - helper functions
"""
import socket
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
import json

from .messages import parse_message

def send_message(target_host: str, target_port: int, message: str):
    """Send a message to a node """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target_host, target_port))
        sock.send(message.encode('utf-8'))
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
        
    send_message(sys.argv[1], int(sys.argv[2]), "Hello")

    parse_message(json.dumps({"test": "test"}).encode('utf-8'))
