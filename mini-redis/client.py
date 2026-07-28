import socket

HOST = "127.0.0.1"
PORT =6379

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST,PORT))
        print("Connected to the server")
        print("Type commands like: SET name beab, GET name, DELETE name")
        print("Type QUIT or EXIT to close the client")

        while True:
            command = input("MiniRedis> ")
            if not command.strip():
                continue
            client_socket.sendall(command.encode())
            response=client_socket.recv(1024).decode().strip()
            print(response)
            if command.upper() in ["EXIT", "QUIT"]:
                break
if __name__ == "__main__":
    start_client()
