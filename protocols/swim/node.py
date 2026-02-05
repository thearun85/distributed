"""
SWIM - Distributed membership protocol - gossip/ infection style implementation
"""
import time

class Node:
    def __init__(self, node_id: str, port: int):
        """Initialize a SWIM node instance"""
        self.node_id = node_id
        self.port = port
        self.running = False

    def start(self):
        """Start the SWIM node instance"""
        print(f"{self.node_id} started on port {self.port}")
        self.running = True

        try:
            while self.running:
                time.sleep(2)

        except KeyboardInterrupt:
            self.running = False
            print(f"Shutting down {self.node_id} running on port {self.port}")


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
