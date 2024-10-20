import socket
import time

# Set up a server
# server_ip = '192.168.1.131'  # Update with the IP address of your server
server_ip = 'rpi3.local'  # Update with the IP address of your server
server_port = 5550

print(f"Connecting to server on port {server_port}")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))
print(f"connected to server with ip {server_ip}")
client_socket.setblocking(0)

while True:
    # Calculate cpu%
    
    message = input("Enter message to send (type 'exit' to quit): ")

    if message == "exit":
        print("Closing connection")
        client_socket.close()
        break

    client_socket.send(message.encode())
    time.sleep(0.005)

    res = ""
    try: 
        res = client_socket.recv(1024).decode()
    except socket.error as e:
        pass
    if res:
        print(res)

