import socket


# Add functions for new programs
def start_maze():
    print("Starting process")

def start_cpu():
    print("Stopping process")

def default_case():
    print("Unknown instruction")

switcher = {
    'maze': start_maze,
    'cpu': start_cpu,
}

def ServerLoop():


    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    host = '0.0.0.0'
    port = 5550

    server_socket.bind((host, port))

    # Listen for a connection only 1 connection
    server_socket.listen(1)

    print("Waiting for client connection...")

    while True:
        # Establish a connection with the client
        client_socket, addr = server_socket.accept()
        print("Got connection from", addr)
        
        try:
            while True:
                # Wait for instructions from the client
                message = client_socket.recv(1024).decode()

                if not message:
                    # If no message is received, break the loop (client disconnected)
                    print("Client disconnected")
                    print("Waiting for client connection...")
                    break
                
                # Print received message
                print("Received:", message)
                
                # Send an acknowledgment back to the client
                action = switcher.get(message, default_case)
                if action != default_case:    
                    client_socket.send(f"Starting program: {message}".encode())
                    action()
                else:
                    client_socket.send("Unknown command received".encode())
        
        except socket.error as e:
            print("Socket error:", e)
        
        finally:
            # Close the client socket when the loop ends
            client_socket.close()





# Main function
if __name__ == "__main__":
    ServerLoop()