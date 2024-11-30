import socket
import pickle


def stop_node(id, port):
    packet_to_send = {"action": "Stop",
                      "source": {"id": 0, "port": 0},
                      "data": ""}
    host = "localhost"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            data_packet = pickle.dumps(packet_to_send)
            print(f'Trying to stop the Node-{id} at port-{port}')
            s.sendall(data_packet)
    except ConnectionRefusedError as e:
        print(f'Failed to stop the Node-{id} at port-{port}')


if __name__ == "__main__":
    stop_node(1, 5001)
    stop_node(2, 5002)
    stop_node(3, 5003)
    stop_node(4, 5004)
    stop_node(5, 5005)
    stop_node(6, 5006)
    stop_node(7, 5007)
    stop_node(8, 5008)
    stop_node(9, 5009)
    stop_node(10, 5010)
