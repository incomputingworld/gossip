:: The number of ports mentioned here should be in sync with the peer_nodes
:: array mentioned in the gossip_process_and_socket.py file.
:: THe program generates the port numbers and store these in an array.

start /b pythonw gossip_process_and_socket.py -id 1 -port 5001
start /b pythonw gossip_process_and_socket.py -id 2 -port 5002
start /b pythonw gossip_process_and_socket.py -id 3 -port 5003
start /b pythonw gossip_process_and_socket.py -id 4 -port 5004
start /b pythonw gossip_process_and_socket.py -id 5 -port 5005
start /b pythonw gossip_process_and_socket.py -id 6 -port 5006
start /b pythonw gossip_process_and_socket.py -id 7 -port 5007
start /b pythonw gossip_process_and_socket.py -id 8 -port 5008
start /b pythonw gossip_process_and_socket.py -id 9 -port 5009
start /b pythonw gossip_process_and_socket.py -id 10 -port 5010