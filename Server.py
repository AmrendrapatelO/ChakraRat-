import socket
import threading

clients = []

# Server setup
server_ip = 'your_server_ip'  # Replace with your server IP
server_port = your_server_port  # Replace with your server port
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, server_port))
server.listen(5)

# Broadcast a message to all connected clients
def broadcast(command):
    for client in clients:
        try:
            client.send(command.encode('utf-8'))
        except:
            pass

# Handle incoming messages from a client
def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(f"Received: {message}")
        except:
            clients.remove(client)
            client.close()
            break

# Accept incoming connections
def accept_connections():
    while True:
        client, addr = server.accept()
        clients.append(client)
        print(f"Connected with {addr}")
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

# Main server function
def start_server():
    print(f"Server running on {server_ip}:{server_port}")
    accept_connections()

# Start the server
start_server()
