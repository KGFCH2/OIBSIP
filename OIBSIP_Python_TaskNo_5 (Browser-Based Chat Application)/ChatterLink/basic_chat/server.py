import socket
import threading

# List to keep track of connected clients
clients = []

def handle_client(client_socket, client_address):
    """
    Handle communication with a single client.
    """
    print(f"New connection from {client_address}")
    clients.append(client_socket)
    
    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received from {client_address}: {message}")
            # Broadcast the message to all other clients
            broadcast(message, client_socket)
        except ConnectionResetError:
            break
    
    # Remove client from list and close connection
    clients.remove(client_socket)
    client_socket.close()
    print(f"Connection from {client_address} closed")

def broadcast(message, sender_socket):
    """
    Send message to all clients except the sender.
    """
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                # Remove broken client
                clients.remove(client)
                client.close()

def main():
    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5555))
    server_socket.listen(5)
    print("Server is listening on port 5555...")
    
    while True:
        # Accept new client connection
        client_socket, client_address = server_socket.accept()
        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    main()