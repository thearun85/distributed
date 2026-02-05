"""
SWIM - Distributed membership protocol - gossip/ infection style implementation
"""
import time
import socket
import threading

import logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

class Node:
    def __init__(self, node_id: str, port: int):
        """Initialize a SWIM node instance"""
        self.node_id = node_id
        self.port = port
        self.running = False # flag to keep the node running continuously

        self.socket = None # tcp socket for accepting connections
        logger.info(f"SWIM node initialized with {self.node_id} and {self.port}")

    def accept_connections(self):
        while self.running:
            self.socket.settimeout(1.0)
            try:
                conn, addr = self.socket.accept()
                logger.info(f"[{self.node_id}] accepted a connection from {addr}")    
                conn.close()
            except socket.timeout:
                pass
            except Exception as e:
                while self.running:
                    logger.error(f"[{self.node_id}] Error while accepting connections: {e}")
    
    def start(self):
        """Start the SWIM node instance"""
        # Bind a socket to the node port and listen for connections
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # in development reuse the port for ease of use
            self.socket.bind(("0.0.0.0", self.port))
            self.socket.listen(5) # Listen for 5 connections backlog
            logger.info(f"SWIM node {self.node_id} listening on port {self.port}")
        except PermissionError as e:
            logger.error(f"Permission denied. Cannot bind to port {self.port} (try port > 1024)")
        except OSError as e:
            if e.errno == 98: # Address already in use
                logger.error(f"[{self.node_id}] Port {self.port} is already in use")
            else:
                logger.error(f"[{self.node_id}] Failed to bind socket: {e}")
            return

        self.running = True

        # a background thread for accepting connections
        accept_thread = threading.Thread(target=self.accept_connections)
        accept_thread.daemon = True
        accept_thread.start()
        
        try:
            while self.running:
                time.sleep(2)

        except KeyboardInterrupt:
            self.running = False
            self.socket.close()
            print(f"[{self.node_id}] Shutting down on port {self.port}")


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: python node.py <node_id> <port>")
        print("press CTRL+C to shutdown")
        sys.exit(1)

    node_id = sys.argv[1]
    port = int(sys.argv[2])
    node = Node(node_id, port)
    node.start()
