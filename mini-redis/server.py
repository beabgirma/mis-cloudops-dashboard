import socket 
from commands import execute_command
from store import MiniRedisStore

HOST = "127.0.0.1"
PORT =6379
store = MiniRedisStore()

def start_server():
    store=MiniRedisStore()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST,PORT))
    server_socket.listen()

    while True:
        client_socket, address=server_socket.accept()
        print(f"Connected by {address}")

        with client_socket:
            while True:
                data=client_socket.recv(1024)
                if not data:
                    break
                command_line=data.decode("utf-8").strip()
                if command_line.upper() in ["QUIT", "EXIT"]:
                    client_socket.sendall("Goodbye!\n".encode())
                    break
                response=execute_command(command_line,store)
                client_socket.sendall((response+ "\n").encode())
if __name__ == "__main__":
    start_server()


