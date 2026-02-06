"""
SWIM - Distributed systems gossip protocol - Observe the members for a running node instance
"""
from flask import Flask, jsonify
from flask_cors import CORS
import threading
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Observer:
    def __init__(self, node, port: int ):
        """Initialize the observer instance"""
        self.node = node # Node instance which is being observed
        self.port = port # port for the flask endpoint
        self.app = Flask(__name__)
        CORS(self.app)

        @self.app.route("/state", methods=['GET'])
        def get_members_state():
            """Return all the node members and their states"""
            members = {}
            for m_id, m in self.node.membership.members.items():
                members[m_id] = {
                    "state": m['state'],
                    "host": m["host"],
                    "port": m['port'],
                }
            return jsonify({
                "node": self.node.node_id,
                "port": self.node.port,
                "members": members,
            }), 200
        
    def start(self):
        """Start the observer instance"""
        observer_thread = threading.Thread(
            target= lambda: self.app.run(host="0.0.0.0",
                                port=self.port,
                                debug=True,
                                use_reloader=False)
        )
        observer_thread.daemon = True
        observer_thread.start()
        logger.info(f"[{self.node.node_id} Observer started]")
