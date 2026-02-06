"""
SWIM - Distributed systems gossip protocol - Membership list implementation
"""
import logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

class MembershipList:
    def __init__(self, local_node_id: str):
        """Initialize the membership object with the local node"""
        self.local_node_id = local_node_id
        self.members = {} # {'node_id': {'state': 'ALIVE', 'last_seen': timestamp, 'suspect_since': timestamp}}
        logger.info(f"[Membership] {self.local_node_id} initialized")

    
