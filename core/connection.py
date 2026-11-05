import socket
from config.settings import BUFFER_SIZE  

class Connection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        return self.sock.getsockname()

    def send(self, data: str | bytes):
        if isinstance(data, str):
            data = data.encode()
        self.sock.sendall(data)

    def recv(self, size: int) -> str:
        return self.sock.recv(size).decode(errors="replace").strip()

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None
