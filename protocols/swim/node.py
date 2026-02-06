"""
SWIM - Distributed membership protocol - gossip/ infection style implementation
"""
import time
import socket
import threading
import random

import logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

from .messages import create_ping, create_ack, parse_message
from .membership import MembershipList

class Node:
    def __init__(self, node_id: str, port: int, peers: list[tuple[str, int]]):
        """Initialize a SWIM node instance"""
        self.node_id = node_id
        self.port = port
        self.running = False # flag to keep the node running continuously

        self.socket = None # tcp socket for accepting connections

        self.sequence = 0 # to track the pings

        self.peers = peers # list of peer tuples
        self.membership = MembershipList(self.node_id)
        logger.info(f"SWIM node initialized with {self.node_id} and {self.port}")
    
    def accept_connections(self):
        """Accept incoming connections"""
        while self.running:
            self.socket.settimeout(1.0)
            try:
                conn, addr = self.socket.accept()
                logger.info(f"[{self.node_id}] accepted a connection from {addr}")    
                handle_thread = threading.Thread(target=self.handle_connections, args=(conn, addr))
                handle_thread.daemon = True
                handle_thread.start()
                
            except socket.timeout:
                pass
            except Exception as e:
                if self.running:
                    logger.error(f"[{self.node_id}] Error while accepting connections: {e}")

    def handle_connections(self, conn, addr):
        """Handle individual connection"""
        conn.settimeout(5.0)
        try: 
            while self.running:
                try:
                    data = conn.recv(1024)
                except socket.timeout as e:
                    logger.info(f"[{self.node_id}] handle_connection timed out for {addr}")
                    break
                    
                if not data:
                    break
                message_str = data.decode('utf-8')
                message = parse_message(message_str)
                logger.info(f"[{self.node_id}] Parsed message is {message}")
                if message:
                    self.membership.mark_alive(message['sender'])
                    if message.get("type", "UNKNOWN") == 'PING':
                    
                        reply = create_ack(self.node_id, message['sequence'])
                        conn.send(reply.encode('utf-8'))
                        logger.info(f"[{self.node_id}] Sent acknowledgement to {addr}")
                
            logger.info(f"[{self.node_id}] {addr} disconected")
        except Exception as e:
            logger.error(f"[{self.node_id}] Exception while reading data: {e}")
        finally:
            conn.close()
            logger.info(f"[{self.node_id}] closing the connection for {addr}")

    def send_ping(self, target_peer: str, target_host: str, target_port: int):
        """Send a PING message to a specified node"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((target_host, target_port))
            self.sequence+=1
            message = create_ping(self.node_id, self.sequence)
            sock.send(message.encode('utf-8'))

            data = sock.recv(1024)
            if data:
                message = parse_message(data.decode('utf-8'))
                if message and message['type'] == 'ACK':
                    logger.info(f"[{self.node_id}] Received acknowledgement from {message['sender']}")
                    self.membership.mark_alive(message['sender'])
        except socket.timeout as e:
            logger.error("[{self.node_id}] - send_ping timed out: {e}")
            self.membership.mark_suspect(target_peer)
        except ConnectionRefusedError as e:
            logger.error(f"[{self.node_id}] - send_ping target node connection error : {e}")
            self.membership.mark_suspect(target_peer)
        except Exception as e:
            logger.error(f"[{self.node_id}] send_ping exception: {e}")
            self.membership.mark_suspect(target_peer)
        finally:
            sock.close()

    def periodic_ping(self):
        """Periodically ping a random peer"""
        logger.info(f"[{self.node_id}] Periodic ping thread started")
        while self.running:
            time.sleep(3.0)
            if self.peers:
                target_peer, target_host, target_port = random.choice(self.peers)
                self.send_ping(target_peer, target_host, target_port)
                logger.info(f"[{self.node_id}] Periodic ping sent to {target_peer}:{target_host}:{target_port}")
        
    def start(self):
        """Start the SWIM node instance"""
        # Bind a socket to the node port and listen for connections
        
        try:
            for peer_id, peer_host, peer_port in self.peers:
                self.membership.add_member(peer_id, peer_host, peer_port)

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

        periodic_thread = threading.Thread(target=self.periodic_ping)
        periodic_thread.daemon = True
        periodic_thread.start()

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
        print("Usage: python node.py <node_id> <port> <host:port>(peers)")
        print("press CTRL+C to shutdown")
        sys.exit(1)

    node_id = sys.argv[1]
    port = int(sys.argv[2])
    peers = []
    print(f"Length of arguments is {len(sys.argv)}")
    if len(sys.argv) > 3:
            
        peers_list = sys.argv[3:]
        print(f"no of peers are {len(peers_list)}")
        for peer in peers_list:
            peer_id, peer_host, peer_port = peer.split(":")
            print(f"processing {peer} {peer_host} {peer_port}")
            if not peer_id or not peer_host or not peer_port:
                raise ValueError(f"Invalid peer {peer}! Peers must in the format 'node:host:port'")
            if not isinstance(peer_id, str):
                raise ValueError(f"Invalid host for {peer}! Peer id must be a string")
            if not isinstance(peer_host, str):
                raise ValueError(f"Invalid host for {peer}! Peer host must be a string")

            try:
                peer_port = int(peer_port)
            except Exception as e:
                print(f"Invalid port {peer}! Peer port must be an integer")
                raise ValueError(f"Invalid port {peer}! Peer port must be an integer")
            peers.append((peer_id, peer_host, peer_port))
            print(f"Peer {peer} validated")
    
    node = Node(node_id, port, peers)
    node.start()
