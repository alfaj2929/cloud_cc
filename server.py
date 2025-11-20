import socket
# Server configuration
HOST = '0.0.0.0'   # Localhost
PORT = 9000         # Port to listen on (non-privileged ports are > 1023)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server started and listening on {HOST}:{PORT}")

conn, addr = server_socket.accept()
print(f"Connected by {addr}")

while True:
    
    data = conn.recv(1024)
    if not data:
        break
  
    message = data.decode()
    print(f"Received from client: {message}")

  
    response = message.upper()
    conn.sendall(response.encode())

conn.close()
server_socket.close()
print("Server closed.")
