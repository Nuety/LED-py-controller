import socket
import subprocess
import psutil

# Add functions for new programs
def start_maze():
    print("Starting maze")

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

def start_cpu():
    client_socket.send("Starting cpu reader".encode())
    print("Starting cpu")
    script_path = 'scripts/startcpu.sh'
    global process
    process = subprocess.Popen(script_path, shell=True)

def stop_process():
    client_socket.send("Stopping running process".encode())
    print("Stopping CPU")
    if process:
        # Terminate the process
        kill(process.pid)
        # process.terminate()  # Graceful termination
        # try:
        #     process.wait(timeout=5)  # Wait for the process to terminate
        #     print("CPU process terminated successfully.")
        # except subprocess.TimeoutExpired:
        #     process.kill()  # Forcefully kill if it doesn't terminate
        #     print("CPU process killed forcefully.")
    else:
        print("No CPU process running.")

def default_case():
    client_socket.send("Unknown command received".encode())
    print("Unknown instruction")


switcher = {
    'maze': start_maze,
    'cpu': start_cpu,
    'stop': stop_process
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
        global client_socket
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
                action()


        
        except socket.error as e:
            print("Socket error:", e)
            process.terminate()
        
        finally:
            # Close the client socket when the loop ends
            client_socket.close()





# Main function
if __name__ == "__main__":
    ServerLoop()