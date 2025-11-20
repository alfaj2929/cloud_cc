import socket

# Server configuration (same as server)
HOST = '127.0.0.1'
PORT = 9000

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print("Connected to server. Type 'exit' to quit.\n")

while True:
    message = input("Enter message: ")
    if message.lower() == 'exit':
        break

    # Send message to server
    client_socket.sendall(message.encode())

    # Receive response
    data = client_socket.recv(1024)
    print(f"Server replied: {data.decode()}")

client_socket.close()
print("Connection closed.")
