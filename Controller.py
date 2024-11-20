import socket
import subprocess
import psutil

# Add functions for new programs
def start_dfmaze():
    print("Starting maze")
    client_socket.send("Starting Depth First Maze".encode())
    script_path = 'scripts/startdfmaze.sh'
    global process
    process = subprocess.Popen(['bash', script_path])

def start_dfamogusmaze():
    print("Starting maze")
    client_socket.send("Starting Depth First Amogus Maze".encode())
    script_path = 'scripts/startdfamogusmaze.sh'
    global process
    process = subprocess.Popen(['bash', script_path])

def start_wfcmaze():
    print("Starting maze")
    client_socket.send("Starting Wave Front Collapse Maze".encode())
    script_path = 'scripts/startwfcmaze.sh'
    global process
    process = subprocess.Popen(['bash', script_path])

def start_wfcamogusmaze():
    print("Starting maze")
    client_socket.send("Starting Wave Front Collapse Amogus Maze".encode())
    script_path = 'scripts/startwfcamogusmaze.sh'
    global process
    process = subprocess.Popen(['bash', script_path])

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
    process = subprocess.Popen(['bash', script_path])

def stop_process():
    if process:
        client_socket.send("Stopping running process".encode())
        print("Stopping running process")
        kill(process.pid)
    else:
        client_socket.send("No process running".encode())
        print("No process running.")

def default_case():
    client_socket.send("Unknown command received\nUse either\ndfmaze for depth first maze\ndfamogusmaze for depth first among us solver\nwfcmaze for wave front collapse maze\nwfcamogusmaze for wave front collapse among us solver\ncpu to start cpu reader\nstop to stop the server".encode())
    print("Unknown instruction")



switcher = {
    'dfmaze': start_dfmaze,
    'dfamogusmaze': start_dfamogusmaze,
    'wfcmaze': start_wfcmaze,
    'wfcamogusmaze': start_wfcamogusmaze,
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