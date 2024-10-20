import socket


# Add functions for new programs
def start_maze():
    print("Starting process")

def start_cpu():
    print("Stopping process")

def default_case():
    print("Unknown instruction")


def ServerLoop():

    switcher = {
        'Maze': start_maze,
        'cpu': start_cpu,
    }

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
                message = client_socket.recv(1024)
                
                if not message:
                    # If no message is received, break the loop (client disconnected)
                    print("Client disconnected")
                    break
                
                # Print received message
                print("Received:", message)
                
                # Send an acknowledgment back to the client
                action = switcher.get(message, default_case)
                if action != default_case:    
                    client_socket.send(f"Starting program: {message}")
                    action()
                else:
                    client_socket.send(f"Unknown command received")
        
        except socket.error as e:
            print("Socket error:", e)
        
        finally:
            # Close the client socket when the loop ends
            client_socket.close()

    # Close the server socket (optional in this example since it's infinite)
    # server_socket.close()




# Main function
if __name__ == "__main__":
    ServerLoop()