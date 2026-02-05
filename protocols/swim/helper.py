"""
SWIM - Distributed protocol - helper functions
"""
import socket
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import json
import random

from .node import Node

    
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: python helper.py <node_id> <port> <host:port>(peer)")
        sys.exit(1)
    node_id = sys.argv[1]
    port = int(sys.argv[2])
    peer_host, peer_port = sys.argv[3].split(":")
    node = Node(node_id, port)
    node.send_ping(peer_host, int(peer_port))
