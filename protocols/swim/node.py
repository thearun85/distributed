"""
SWIM - Distributed membership protocol - gossip/ infection style implementation
"""


class Node:
    def __init__(self, node_id: str):
        """Initialize a SWIM node instance"""
        self.node_id = node_id

    def start(self):
        """Start the SWIM node instance"""
        print(f"{self.node_id} started")



if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python node.py <node_id>")
        sys.exit(1)

    node_id = sys.argv[1]
    node = Node(node_id)
    node.start()
