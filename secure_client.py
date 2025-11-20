import socket
from cryptography.fernet import Fernet

# Load the same symmetric key used by server
with open("secret.key", "rb") as f:
    key = f.read()

cipher = Fernet(key)

# Server configuration
HOST = '127.0.0.1'
PORT = 65432

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print("Connected to server. Type 'exit' to quit.\n")

while True:
    message = input("Enter message: ")
    if message.lower() == 'exit':
        break

    # ----------- ENCRYPT message before sending -----------
    encrypted_message = cipher.encrypt(message.encode())
    client_socket.sendall(encrypted_message)

    # ----------- Receive and DECRYPT server reply -----------
    encrypted_reply = client_socket.recv(1024)
    reply = cipher.decrypt(encrypted_reply).decode()

    print(f"Server replied (decrypted): {reply}")

client_socket.close()
print("Connection closed.")
