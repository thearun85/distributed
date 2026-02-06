"""
SWIM - Distributed systems gossip protocol - Membership list implementation
"""
import time
import logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

class MembershipList:
    def __init__(self, local_node_id: str):
        """Initialize the membership object with the local node"""
        self.local_node_id = local_node_id
        self.members = {} # {'node_id': {'host':'localhost', 'port': 5001, state': 'ALIVE', 'last_seen': timestamp, 'suspect_since': timestamp}}
        logger.info(f"[Membership] {self.local_node_id} initialized")

    
    def add_member(self, node_id: str, host: str, port: int):
        """Add a new member to the membership group"""
        if node_id not in self.members:
            self.members[node_id] = {
                "state": 'ALIVE',
                "host": host,
                "port": port,
                "last_seen": time.time(),
            }
            logger.info(f"[Membership]-{self.local_node_id}: Member {node_id}:{host}:{port} added to the group")
