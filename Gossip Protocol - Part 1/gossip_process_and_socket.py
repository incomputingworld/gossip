import socket
import threading
import random
import time
import pickle
import logging
import argparse


# Each node runs as a server and a client to exchange gossip

class Node:
    def __init__(self, id, port, peers):
        self.id = id
        self.data = {f"info-{id}"}  # Initial data for the node
        self.port = port
        self.peers = peers  # List of peer (IP, port) pairs
        self.logger = None
        self.running = True

        self.init_logger()
        self.start_listener_thread()
        self.start_gossip_thread()

    def init_logger(self):
        # Create a log file for each node.
        self.logger = logging.getLogger(f'Node{self.id}')
        self.logger.setLevel(logging.INFO)
        log_file = f'logs/Node_{self.id}_log.log'
        f_handle = logging.FileHandler(log_file)
        f_handle.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
        f_handle.setFormatter(formatter)
        self.logger.addHandler(f_handle)

    def start_listener_thread(self):
        # Start the server to listen for gossip from peers
        listener_thread = threading.Thread(target=self.listen_to_nodes)
        listener_thread.start()

    def listen_to_nodes(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("localhost", self.port))
        server_socket.listen(10)
        print(f"Node {self.id} listening on port {self.port}")
        self.logger.info(f"Node {self.id} listening on port {self.port}")

        while self.running:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=self.handle_peer, args=(client_socket, client_address,))
            client_thread.start()

        server_socket.close()
        self.logger.info(f"Node {self.id} listener stopped.")
        self.logger.info(f"Node {self.id} updated data: {self.data}")

    def handle_peer(self, client_socket, client_address):
        # Receive and update data from a peer
        packet = client_socket.recv(1024)
        peer_data = pickle.loads(packet)
        action = peer_data["action"]
        print(f"Node - {self.id} - action {peer_data['action']} - from Node - {peer_data['source']['id']}")
        self.logger.info(f"Node - {self.id} - action {peer_data['action']} - from Node - {peer_data['source']['id']}")

        if "gossip" == action:
            self.data = self.data.union(peer_data["data"])  # Merge the data

        elif "Stop" == action:
            self.stop()
            self.logger.info(f"Node {self.id} stopping...")

        client_socket.close()

    def start_gossip_thread(self):
        # Start the server to gossip with peers at random interval
        gossip_thread = threading.Thread(target=self.start_gossip)
        gossip_thread.start()

    def start_gossip(self):
        while self.running:
            time.sleep(random.uniform(1, 5))  # Random gossip interval
            self.gossip()
        self.logger.info(f"Node {self.id} Gossip stopped.")

    def gossip(self):
        # Select a random peer to gossip with
        peer = random.choice(self.peers)
        peer_ip, peer_port = peer
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((peer_ip, peer_port))
                packet_to_send = {"action": "gossip",
                                  "source": {"id": self.id, "port": self.port},
                                  "data": self.data}
                packet = pickle.dumps(packet_to_send)
                s.sendall(packet)
                print(f"Node {self.id} gossiped with peer Node at port {peer_port}")
                self.logger.info(f"Node {self.id} gossiped with peer Node at port {peer_port}")
        except ConnectionRefusedError:
            print(f"Node {self.id} failed to connect to Node at port {peer_port}")
            self.logger.info(f"Node {self.id} failed to connect to Node at port {peer_port}")

    def stop(self):
        self.running = False


def manage_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-id', type=str, help='Process ID')
    parser.add_argument('-port', type=int, help='Port')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    # The value of num_nodes should be in sync with the number of processes we wish to start.
    # The value of base_port should align with the port number we mention in the .bat file while starting the process.
    # I use these two variables to generate the list of peers (id and port) which is shared with each node.
    # The file accepts two command line arguments, id and port when the node starts.
    # Refer start_nodes.bat file

    args = manage_arguments()
    if args.id is None or args.port is None:
        print("Missing Process ID or port number")
        exit()
    print(args.port)
    num_nodes = 10
    base_port = 5000
    peer_nodes = [(f"localhost", base_port + j) for j in range(1, num_nodes+1) if j+base_port != args.port]
    node = Node(id=args.id, port=args.port, peers=peer_nodes)

