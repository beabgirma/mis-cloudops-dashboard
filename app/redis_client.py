import socket

def send_redis_command(command: str) -> str:
    """Opens a raw TCP socket, sends a command to Mini Redis, and reads the response."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 6379))
        
        # Append the newline character your server parsing logic expects
        payload = f"{command}\n"
        s.sendall(payload.encode("utf-8"))
        
        response = s.recv(1024).decode("utf-8").strip()
        s.close()
        return response
    except ConnectionRefusedError:
        return "REDIS_DOWN"