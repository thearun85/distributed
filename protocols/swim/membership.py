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
        self.suspect_timeout = 5.0 # Suspect timeout to mark a member as DEAD
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

    def mark_alive(self, node_id):
        """Mark a member ALIVE on receiving an acknowledgement"""
        if node_id in self.members:
            self.members[node_id]['state'] = 'ALIVE'
            self.members[node_id]['last_seen'] = time.time()
            self.members[node_id]['suspect_since'] = None  

    def mark_suspect(self, node_id):
        """Mark a member as SUSPECT on not receiving an acknowledgement"""
        if node_id in self.members :
            self.members[node_id]['state'] = 'SUSPECT'
            self.members[node_id]['suspect_since'] = time.time()   




    def get_alive_members(self):
        """Get all the members marked as ALIVE"""
        return [members for member_id, members in self.members.items() if members['state'] == 'ALIVE']
