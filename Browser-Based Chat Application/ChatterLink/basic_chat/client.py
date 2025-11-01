import socket
import threading

def receive_messages(client_socket):
    """
    Continuously receive and print messages from the server.
    """
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except ConnectionResetError:
            print("Connection lost.")
            break

def main():
    # Create client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to server
        client_socket.connect(('127.0.0.1', 5555))
        print("Connected to server. Type your messages:")
        
        # Start thread to receive messages
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()
        
        # Send messages
        while True:
            message = input()
            if message.lower() == 'quit':
                break
            client_socket.send(message.encode('utf-8'))
    
    except ConnectionRefusedError:
        print("Could not connect to server. Make sure the server is running.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()